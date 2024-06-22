#users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics,permissions
from .serializers import CustomUserSerializer,PostSerializer,SubscriptionSerializer
from .utils import generate_otp, send_otp_email
from .models import CustomUser,Post,Subscription,Block
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny,IsAuthenticatedOrReadOnly
from .serializers import UserSerializer,BlockSerializer

class VerifyOTP(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp_entered = request.data.get('otp')

        try:
            user = CustomUser.objects.get(email=email, otp=otp_entered)
            user.is_verified=True

            user.save()

            return Response({'message': 'Email verified successfully.'},
                              status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

class UserRegistration(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            otp = generate_otp()
            user.otp = otp
            user.save()

            send_otp_email(user.email, otp)

            return Response({'message': 'User registered successfully. OTP sent to your email.'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#
class LoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)

        if not user:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            'username': user.username,
            'email': user.email,
            'access_token': access_token,
            'refresh_token': str(refresh)
        }, status=status.HTTP_200_OK)


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user and request.user.is_authenticated

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            blocked_users = Block.objects.filter(blocker=user).values_list('blocked_user', flat=True)
            users_who_blocked_me = Block.objects.filter(blocked_user=user).values_list('blocker', flat=True)
            queryset = Post.objects.exclude(author__in=blocked_users).exclude(author__in=users_who_blocked_me)
        else:
            queryset = Post.objects.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            blocked_users = Block.objects.filter(blocker=user).values_list('blocked_user', flat=True)
            users_who_blocked_me = Block.objects.filter(blocked_user=user).values_list('blocker', flat=True)
            queryset = Post.objects.exclude(author__in=blocked_users).exclude(author__in=users_who_blocked_me)
        else:
            queryset = Post.objects.all()
        return queryset

class SubscriptionListCreateView(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(subscriber=self.request.user)

class SubscriptionDetailView(generics.RetrieveDestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(subscriber=self.request.user)

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class BlockUserView(generics.CreateAPIView):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        blocked_user = CustomUser.objects.get(id=self.request.data['blocked_user'])
        serializer.save(blocker=self.request.user, blocked_user=blocked_user)

class UnblockUserView(generics.DestroyAPIView):
    queryset = Block.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        blocked_user = CustomUser.objects.get(id=self.request.data['blocked_user'])
        return Block.objects.get(blocker=self.request.user, blocked_user=blocked_user)
