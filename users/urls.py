from django.urls import path
from users.views import UserRegistration,VerifyOTP,LoginAPI,PostListCreateView, PostDetailView,SubscriptionDetailView,SubscriptionListCreateView,UserListView,BlockUserView,UnblockUserView


urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('verify/', VerifyOTP.as_view(), name='verify'),
    path('login/',LoginAPI.as_view(),name='login'),
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('subscriptions/', SubscriptionListCreateView.as_view(), name='subscription-list-create'),
    path('subscriptions/<int:pk>/', SubscriptionDetailView.as_view(), name='subscription-detail'),
    path('blocks/', BlockUserView.as_view(), name='block-user'),
    path('unblocks/', UnblockUserView.as_view(), name='unblock-user'),




]