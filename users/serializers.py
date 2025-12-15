from rest_framework import serializers
from django.contrib.auth import get_user_model
import re

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'university'] # University eklendi

    def validate_username(self, value):
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError("Kullanıcı adı sadece harf, rakam ve alt tire içerebilir.")
        if len(value) < 3:
            raise serializers.ValidationError("Kullanıcı adı en az 3 karakter olmalıdır.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Şifre en az 8 karakter olmalıdır.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Bu e-posta adresi zaten kullanımda.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user