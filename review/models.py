from django.db import models
from django.contrib.auth import get_user_model
from posts.models import Post

User=get_user_model()

class Like(models.Model):
    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    user=models.ForeignKey(User,related_name='likes',on_delete=models.CASCADE)
    post=models.ForeignKey(Post,related_name='likes',on_delete=models.CASCADE)


class Comment(models.Model):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    user=models.ForeignKey(User,related_name='comments',on_delete=models.CASCADE)
    post=models.ForeignKey(Post,related_name='cooments',on_delete=models.CASCADE)
    body=models.TextField()

    created_at=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now=True)



class Favorite(models.Model):
    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True) 


class Rating(models.Model):
    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
    rating = models.IntegerField()  
    created_at = models.DateTimeField(auto_now_add=True)
