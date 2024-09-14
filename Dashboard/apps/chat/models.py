from django.db import models
from apps.users.models import CustomUser
# Create your models here.
class Conversation(models.Model):
    user1 = models.ForeignKey(CustomUser, related_name='user1_conversations', on_delete=models.CASCADE)
    user2 = models.ForeignKey(CustomUser, related_name='user2_conversations', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user1', 'user2'],
                name='unique_conversation',
                condition=models.Q(
                    user1__lt=models.F('user2')
                )
            )
        ]
    
    def __str__(self):
        return f"Conversation between {self.user1.first_name} and {self.user2.first_name}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    is_received = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.sender.username} in conversation {self.conversation.id}"


class File(models.Model):
  message = models.OneToOneField(Message, on_delete=models.CASCADE, related_name='file')
  file = models.FileField(upload_to='chat_file')
  
  def __str__(self):
      return f"File attached to message {self.message.id}"