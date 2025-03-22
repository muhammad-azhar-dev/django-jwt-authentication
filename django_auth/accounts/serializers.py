from rest_framework import serializers
from .models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util

# User registration serializer
class UserRegisterationSerializer(serializers.ModelSerializer):
    # we are writing this: becz we need confirm password field in our Registration Request
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2', 'tc']
        extra_kwargs = {
            'password': {'write_only':True}
        }

    # Validate password and confirm password while Rrgistration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match!")
        
        return attrs
    
    # for creating User becz, we create custom user 
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)

# User Login Serializer    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']

# User Profile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']

# User Change Password Serializer
class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['password','password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm password doesn't match")
        user.set_password(password)
        user.save()
        return attrs

# Send Email Serializer (for reset password)    
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']
    
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print("Encoded uid: ", uid)

            token = PasswordResetTokenGenerator().make_token(user)
            print("Password Reset Token: ", token)

            link = f"http://127.0.0.1:8000/api/user/reset-password/{uid}/{token}"
            print("Password Reset Link: ", link)
            
            # Send Email 
            data = {
                'email_subject': 'Reset Password',
                'email_body': f'Click the link below to reset your password\nYou have only 15 minutes\n{link}',
                'to_email': user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError("User with this email doesn't exists")

# User Password Reset Serializer        
class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['password','password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token') 
            if password != password2:
                raise serializers.ValidationError("Password and Confirm password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("Token is not valid or expired")
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            raise serializers.ValidationError("Token is not valid or expired")