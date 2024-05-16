from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Post(models.Model):
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


    author = models.ForeignKey(User,
                               on_delete=models.CASCADE, 
                               related_name='posts', 
                               verbose_name='Автор',
                               blank=True)
    
    title = models.CharField(max_length= 60, 
                             verbose_name= 'Название')
    
    content = models.TextField(blank=True,
                               verbose_name= 'Описание')

    created_at = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(upload_to='media/',
                              blank=True,
                              verbose_name='Фото')



    def __str__(self):
        return self.title