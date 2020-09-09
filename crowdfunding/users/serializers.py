from rest_framework import serializers
from .models import CustomUser, UserProfile

class ProfileSerializer(serializers.Serializer):
    profile_image_url = serializers.URLField()
    user_bio = serializers.CharField(max_length=200)


class CustomUserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)
    profile = ProfileSerializer(required=False)
    password = serializers.CharField(write_only=True, max_length=100)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        profile = validated_data.pop('profile')

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        if not hasattr(instance, 'profile'):
            # Create pro
            UserProfile.objects.create(**profile, user=instance)
        else:
            instance.profile.user_bio = profile.get('user_bio', instance.profile.user_bio)
            instance.profile.profile_image_url = profile.get(
                'profile_image_url', instance.profile.profile_image_url)
            instance.profile.save()

        return instance

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(write_only=True, max_length=100)