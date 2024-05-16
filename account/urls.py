from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterView, ActivationView, PasswordReset, PasswordResetView


urlpatterns = [
    path("register/", RegisterView.as_view()),
    path(
        "activate/<str:email>/<str:activation_code>/",
        ActivationView.as_view(),
        name="activate",
    ),
    path("login/", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("password_reset/", PasswordReset.as_view()),
    path(
        "password_reset/<str:pk>/<str:token>/",
        PasswordResetView.as_view(),
        name="password_reset",
    ),
]