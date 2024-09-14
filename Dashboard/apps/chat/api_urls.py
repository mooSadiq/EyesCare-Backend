from django.urls import path
from . import mobile_api

urlpatterns = [
    path('conversations/', mobile_api.ConversationList.as_view(), name='conversation-list'), 
    path('conversations/<int:pk>/', mobile_api.ConversationDetails.as_view(), name='conversation-detail'), 
    path('conversations/delete/<int:pk>/', mobile_api.ConversationList.as_view(), name='conversation-delete'), 
    path('messages/<int:conversation_id>/', mobile_api.MessageList.as_view(), name='message-list'),  
    path('messages/send/', mobile_api.MessageList.as_view(), name='message-create'), 
]
