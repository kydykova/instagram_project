from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model

class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.email', read_only=True)
    class Meta:
        model = Post
        fields = '__all__'


    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        post = super().create(validated_data)
        post.save()
        return post

from account.models import User 

class PostListSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.email', read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'image', 'author') 