#users/serializers.py
from rest_framework import serializers
from .models import CustomUser,Post,Subscription,Block

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', )
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Post
        fields = '__all__'


    def validate(self, data):
        author = data.get('author')
        if author:
            blocked_users = CustomUser.objects.filter(blocked_by_authors=author)
            if blocked_users.exists():
                raise serializers.ValidationError(
                    f"Cannot create post. Author is blocked by {blocked_users.count()} users.")
        return data
class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']

class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ['id', 'blocker', 'blocked_user']
        read_only_fields = ['blocker']
