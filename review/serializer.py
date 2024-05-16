from rest_framework.serializers import ModelSerializer
from .models import Comment,Favorite,Rating

# from rest_framework import serializers
# from .models import Post


class CoomentSerializer(ModelSerializer):
    class Meta:
        model=Comment
        exclude=['user']

    def validate(self, attrs):
        super().validate(attrs)
        request=self.context.get('request')
        attrs['user']=request.user 
        return attrs
    

class FavoriteSerializer(ModelSerializer):
    class Meta:
        model=Favorite
        exclude=['user']

    def validate(self, attrs):
        super().validate(attrs)
        request=self.context.get('request')
        attrs['user']=request.user 
        return attrs
    

class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'