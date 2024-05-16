from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema

from .serializers import RegisterSerializer, EmailSerializer, PasswordResetSerializer
from .tasks import create_reset_url, send_password_reset_link


User = get_user_model()


class RegisterView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer())
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response("Вы успешно зарегистрировались", 201)


class ActivationView(APIView):
    def get(self, request, email, activation_code):
        user = User.objects.filter(email=email, activation_code=activation_code).first()
        if not user:
            return Response("Пользователь не найден", 404)
        user.activation_code = ""
        user.is_active = True
        user.save()
        return Response("Вы успешно активировали аккаунт")


class PasswordReset(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = User.objects.filter(email=email).first()
        if  not user:
            return Response("Пользователь не найден", 404)
        pk = user.pk
        token = PasswordResetTokenGenerator().make_token(user)
        link = create_reset_url(pk, token)
        send_password_reset_link(email, link)

        return Response(f"Ваша ссылка для изменения пароля {link}",
            200)


class PasswordResetView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = PasswordResetSerializer

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = User.objects.get(pk=pk)
        except:
            return Response("User does not exist", 404)

        serializer = self.serializer_class(
            data=request.data,
            context={"kwargs": kwargs}
        )
        serializer.is_valid(raise_exception=True)

        return Response("Ваш пароль успешно изменён")