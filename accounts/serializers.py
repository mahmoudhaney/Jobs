from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
        'first_name': {'required': True},
        'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
        username=validated_data['username'],
        email=validated_data['email'],
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name']
        )
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["address", "phone_number", "image"]

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "profile"]
        extra_kwargs = {
        'username': {'required': False, 'read_only': True},
        }

    def update(self, instance, validated_data):
        """
        Override serializer 'update' function,
        Because DRF doesn't support Writable Nested Serializers
        """
        # Update User Data
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.save()

        # Update User's Profile Data
        try:
            user_profile = Profile.objects.get(user=instance.id)
            if user_profile:
                user_profile.address= validated_data['profile']['address']
                user_profile.phone_number= validated_data['profile']['phone_number']
                user_profile.image= validated_data['profile']['image']
                user_profile.save()
            return instance
        except Profile.DoesNotExists:
            pass
