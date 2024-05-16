from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from posts.models import Post
# from rest_framework.views import APIView
# from rest_framework import status

from .models import Like,Comment,Favorite,Rating
from .serializer import CoomentSerializer,FavoriteSerializer,RatingSerializer
from .permissions import IsOwnerorReadOnly
# from .serializer import PostSerializer




@api_view(['POST'])
def toggle_like(request,id):
    user=request.user
    if not user.is_authenticated:
        return Response(status=401)
    post=get_object_or_404(Post,id=id)
    if Like.objects.filter(user=user,post=post).exists():
        Like.objects.filter(user=user,post=post).delete()
    else:
        Like.objects.create(user=user,post=post)

    return Response(201)



class CommentViewSet(ModelViewSet):
    queryset=Comment.objects.all()
    serializer_class=CoomentSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        elif self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwnerorReadOnly]
        return [permission() for permission in self.permission_classes]



class FavoriteViewSet(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer  

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated]  # Доступ только зарегистрированным пользователям
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwnerorReadOnly]  # Доступ только владельцам избранных товаров
        return [permission() for permission in self.permission_classes]


class RatingViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]