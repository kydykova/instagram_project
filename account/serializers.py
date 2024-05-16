from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import serializers

from .tasks import send_activation_code, send_password_reset_link, create_reset_url


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=4,
        required=True,
        write_only=True,
    )
    password_confirm = serializers.CharField(
        min_length=4,
        required=True,
        write_only=True,
    )

    class Meta:
        model = User
        fields = "email", "password", "password_confirm"

    def validate(self, attrs):
        p1 = attrs.get("password")
        p2 = attrs.pop("password_confirm")

        if p1 != p2:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        send_activation_code.delay(user.email, user.activation_code)
        return user


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ["email"]


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        min_length=4,
    )

    class Meta:
        fields = ["password"]

    def validate(self, data):
        password = data.get("password")
        token = self.context.get("kwargs").get("token")
        pk = self.context.get("kwargs").get("pk")
        if not token or not pk:
            raise  serializers.ValidationError("Нет данных")
            
        user = User.objects.get(pk=pk)

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("Неверный токен для изменеия")

        user.set_password(password)
        user.save()
        return data