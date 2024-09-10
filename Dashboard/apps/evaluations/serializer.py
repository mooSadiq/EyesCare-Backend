from rest_framework import serializers
from .models import Review
from apps.users.models import CustomUser


class ReviewSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    profile_picture = serializers.ImageField(source='user.profile_picture', read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'user_id', 'first_name', 'last_name', 'email', 'profile_picture', 'rating', 'comment', 'created_at']
    def validate_rating(self, value):
        # التأكد من أن قيمة التقييم لا تتجاوز 5
        if value > 5:
            raise serializers.ValidationError("Rating must be 5 or less.")
        return value