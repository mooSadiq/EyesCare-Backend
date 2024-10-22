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
    
      
# الرسائل 
class MessageSerializer(serializers.ModelSerializer):
    file = serializers.FileField(source='message_file.file', read_only=True)
    time_since = serializers.SerializerMethodField() 
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'content', 'is_read', 'is_received', 'timestamp', 'time_since', 'file']

    def get_time_since(self, obj):
        return timesince(obj.timestamp) 
        
        
        
# المحادثات للتطبيق
class ConversationSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField() 
    last_message = serializers.SerializerMethodField() 
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





# --------------------الداش بورد-----------------------------------------------------------------
class CustomUserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'profile_picture']
        
    def get_profile_picture(self, obj):
        request = self.context.get('request')        
        if request is not None:
            domain = request.get_host()
            if obj.profile_picture:
                return f"http://{domain}{obj.profile_picture.url}"
        return None  
      
      

class ConversationDetailSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True)  
    other_user = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'is_active', 'created_at', 'messages', 'other_user']

    def get_other_user(self, obj):
        request_user = self.context['request'].user
        other_user = obj.user2 if obj.user1 == request_user else obj.user1
        return CustomUserSerializer(other_user, context={'request': self.context['request']}).data 

        
class ContactsAndConversationsSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'profile_picture', 'email', 'last_message']

    def get_last_message(self, user):
        request_user = self.context['request'].user
        conversation = Conversation.objects.filter(
            Q(user1=request_user, user2=user) | Q(user2=request_user, user1=user)
        ).first()
        
        if conversation:
            last_message = conversation.messages.order_by('-timestamp').first()  
            if last_message:
                file_url = last_message.message_file.file.url if hasattr(last_message, 'message_file') and last_message.message_file else None
                time_ago = self.get_time_since(last_message)
                return {
                    'content': last_message.content,  
                    'conversation': last_message.conversation.id,  
                    'timestamp': time_ago,  
                    'sender': last_message.sender.id,  
                    'file': file_url  
                }
        return None   
    def get_time_since(self, obj):
        return timesince(obj.timestamp)



