from rest_framework import serializers
from .models import Conversation, Message, File
from apps.users.models import CustomUser
from django.utils.timesince import timesince
from django.db.models import Q

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
class MessageSerializer(serializers.ModelSerializer):
    file = FileSerializer(read_only=True)
    time_since = serializers.SerializerMethodField()  # حقل الوقت بصيغة "منذ"

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'content', 'is_read', 'is_received', 'timestamp', 'time_since', 'file']

    def get_time_since(self, obj):
        return timesince(obj.timestamp) 
      
class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    other_user = serializers.SerializerMethodField()  # حقل المستخدم الآخر
    last_message = serializers.SerializerMethodField()  # آخر رسالة
    class Meta:
        model = Conversation
        fields = ['id', 'user1', 'user2', 'created_at', 'messages','last_message', 'other_user']
        
    def get_other_user(self, obj):
        # تحديد المستخدم الآخر بناءً على من قام بالطلب
        request_user = self.context['request'].user
        other_user = obj.user1 if obj.user1 != request_user else obj.user2
        return {
            'id': other_user.id,
            'email': other_user.email,
            'first_name': other_user.first_name,
            'last_name': other_user.last_name,
            'profile_picture': other_user.profile_picture.url if other_user.profile_picture else None
        }
    def get_last_message(self, obj):
        last_message = obj.messages.order_by('-timestamp').first()  # جلب آخر رسالة
        return MessageSerializer(last_message).data






class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'profile_picture']
        
class ContactsConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()  # آخر رسالة
    class Meta:
        model = Conversation
        fields = ['id', 'user1', 'user2', 'created_at', 'messages','last_message']
        
    def get_last_message(self, obj):
        last_message = obj.messages.order_by('-timestamp').first()  # جلب آخر رسالة
        return MessageSerializer(last_message).data
        
class ContactsSerializer(serializers.ModelSerializer):
    conversations = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'profile_picture', 'email', 'conversations']

    def get_conversations(self, user):
        request_user = self.context['request'].user
        conversations = Conversation.objects.filter(
            (Q(user1=request_user) & Q(user2=user)) |
            (Q(user2=request_user) & Q(user1=user))
        )
        return ContactsConversationSerializer(conversations, many=True).data if conversations.exists() else None
      