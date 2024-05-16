from django.urls import path,include
from rest_framework.routers import DefaultRouter


from .views import toggle_like,CommentViewSet,FavoriteViewSet,RatingViewSet

# from .views import PostCreateAPIView


router=DefaultRouter()
router.register('comment',CommentViewSet)
router.register('favorite', FavoriteViewSet)
router.register('rating', RatingViewSet)


urlpatterns=[
    path('like/<int:id>/',toggle_like),
    path('',include(router.urls)),
]