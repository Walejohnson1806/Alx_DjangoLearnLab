
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from .models import CustomUser


class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
    )
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password2 = serializers.CharField(write_only=True, required=True)

    token = serializers.SerializerMethodField() # Custom field to return token: Output-only field
    
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'bio', 'token')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        # Remove password2 before creating user
        validated_data.pop('password2') 
        # Create user using create_user method
        user = get_user_model().objects.create_user(**validated_data)
        # Create token for the user
        token = Token.objects.create(user=user)
        return user
    
    def get_token(self, obj):
        token = Token.objects.get(user=obj)
        return token.key
        


class UserProfileSerializer(serializers.ModelSerializer):
    follower_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 
                  'bio', 'profile_picture', 'follower_count', 'following_count', 
                  'date_joined', 'updated_at')
        read_only_fields = ('id', 'date_joined', 'updated_at')        
