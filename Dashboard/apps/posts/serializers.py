from rest_framework import serializers
from .models import Post, PostImage, Like
from apps.users.models import CustomUser
from datetime import datetime
from urllib.parse import urljoin


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'profile_picture']
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'post']

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'post', 'image']

class PostSerializer(serializers.ModelSerializer):
    image = PostImageSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['user', 'text', 'image', 'likes_count', 'views_count', 'created_at']
        read_only_fields = ['user', 'likes_count', 'views_count', 'created_at']
    


class PostListSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    post_id = serializers.IntegerField(source='id', read_only=True)
    name = serializers.SerializerMethodField()
    profile_picture = serializers.ImageField(source='user.profile_picture', read_only=True)
    image_url = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()  


    class Meta:
        model = Post
        fields = ['user_id', 'name', 'profile_picture', 'post_id', 'text', 'image_url', 'likes_count', 'views_count', 'created_at', 'is_liked']
        read_only_fields = ['user_id', 'name', 'profile_picture', 'likes_count', 'views_count', 'created_at', 'is_liked']

    def get_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def get_image_url(self, obj):
        if hasattr(obj, 'image') and obj.image and obj.image.image:
            domain = self.context.get('request').get_host()
            return urljoin(f'http://{domain}', obj.image.image.url)
        return None
      
    def get_created_at(self, obj):
        return obj.created_at.date().isoformat()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user_id=request.user.id).exists()
        return False