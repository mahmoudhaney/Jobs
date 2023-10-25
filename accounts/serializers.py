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
        extra_kwargs = {
        'address': {'required': False},
        'phone_number': {
            'required': False,
            'validators': [
                        UniqueValidator(
                            queryset=Profile.objects.all(),
                            message=("This number already exist"),
                        )
                    ]
            },
        'image': {'required': False,},
        }

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "profile"]
        extra_kwargs = {
        'username': {'required': False, 'read_only': True},
        'email': {
                    'validators': [
                        UniqueValidator(
                            queryset=User.objects.all(),
                            message=("This email already exist"),
                        )
                    ]
                },
        }

    def update(self, instance, validated_data):
        """
        Override serializer 'update' function,
        Because DRF doesn't support Writable Nested Serializers
        """        
        # Update User Data
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        
        # Update User's Profile Data
        try:
            profile = Profile.objects.get(user=instance.id)
            profile_data = validated_data.pop('profile')

            profile.address = profile_data.get('address', profile.address)
            profile.phone_number = profile_data.get('phone_number', profile.phone_number)
            profile.image = profile_data.get('image', profile.image)
            profile.save()
            return instance
        except Profile.DoesNotExists:
            pass
