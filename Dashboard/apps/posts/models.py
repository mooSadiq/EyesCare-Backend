from django.db import models
from apps.users.models import CustomUser
# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(CustomUser, related_name="posts_user", on_delete=models.CASCADE)
    text = models.TextField(null=True)  # نص المنشور
    likes_count = models.IntegerField(default=0)  # عدد الإعجابات
    views_count = models.PositiveIntegerField(default=0)  # عدد مرات مشاهدة المنشور
    created_at = models.DateTimeField(auto_now_add=True)  # تاريخ إنشاء المنشور

    def __str__(self):
        return f"{self.user},{self.created_at}"
      
      
class PostImage(models.Model):
    post = models.OneToOneField(Post, related_name='image', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/')
    
    def __str__(self):
        return f"{self.post}"
      
class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')
        
    def __str__(self):
        return f"{self.user},{self.post}"
