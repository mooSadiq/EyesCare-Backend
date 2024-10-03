from rest_framework import serializers
from .models import Conversation, Message, File
from apps.users.models import CustomUser
from django.utils.timesince import timesince
from django.db.models import Q
from urllib.parse import urljoin


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
        
class MessageSerializer(serializers.ModelSerializer):
    file = serializers.FileField(source='message_file.file', read_only=True)
    time_since = serializers.SerializerMethodField()  # حقل الوقت بصيغة منذ

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'content', 'is_read', 'is_received', 'timestamp', 'time_since', 'file']

    def get_time_since(self, obj):
        return timesince(obj.timestamp) 
      
      
class ConversationSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()  # حقل المستخدم الآخر
    last_message = serializers.SerializerMethodField()  # آخر رسالة
    unread_messages_count = serializers.SerializerMethodField()  
    class Meta:
        model = Conversation
        fields = ['id', 'user1', 'user2', 'created_at','last_message','unread_messages_count', 'other_user', 'is_active']
        
    def get_other_user(self, obj):
        request_user = self.context['request'].user
        other_user = obj.user1 if obj.user1 != request_user else obj.user2
        domain = self.context.get('request').get_host()
        return {
            'id': other_user.id,
            'email': other_user.email,
            'first_name': other_user.first_name,
            'last_name': other_user.last_name,
            'profile_picture': urljoin(f'http://{domain}', other_user.profile_picture.url) if other_user.profile_picture else None
        }
                        
    def get_last_message(self, obj):
        last_message = obj.messages.order_by('-timestamp').first()  # جلب آخر رسالة
        domain = self.context['request'].get_host()
        file_url = None
        if hasattr(last_message, 'message_file') and last_message.message_file:
            file_url = urljoin(f'http://{domain}', last_message.message_file.file.url)
        message_data = MessageSerializer(last_message).data
        message_data['file'] = file_url if file_url else None        
        return message_data

    def get_unread_messages_count(self, obj):
        request_user = self.context['request'].user
        other_user = obj.user1 if obj.user1 != request_user else obj.user2
        unread_count = obj.messages.filter(is_read=False, sender=other_user).count()
        return unread_count






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
      