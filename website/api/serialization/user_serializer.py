from rest_framework import serializers
from website.models import AuthUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ['id', 'username', 'email', 'is_superuser', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # never return password
        }

    def create(self, validated_data):
        # Use Django's create_user to hash password
        password = validated_data.pop('password', None)
        user = AuthUser(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
