from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializers(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    username = serializers.CharField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        """Parollarni tekshirish va mavjud foydalanuvchilarni tekshirish"""
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password": "Parollar mos kelmadi"})

        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Bu username allaqachon band"})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Bu email allaqachon ishlatilgan"})

        return data

    def create(self, validated_data):
        """Foydalanuvchini yaratish"""
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password1'],
            is_active=False
        )
        return user
