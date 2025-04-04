
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import CustomUser


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150) 
    bio = serializers.CharField(allow_blank=True, required=False)
    followers_count = serializers.IntegerField(source="followers.count", read_only=True)
    following_count = serializers.IntegerField(source="following.count", read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers_count', 'following_count']
        

class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)  
    email = serializers.CharField(max_length=255)  
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user
    
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio', 'profile_picture', 'followers']
        read_only_fields = ['username', 'followers']
