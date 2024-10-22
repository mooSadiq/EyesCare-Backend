from django.urls import path
from . import views
from . import mobile_api
urlpatterns = [
    path('', views.chatview, name="chat_list"),
    path('api/conversations/send/', views.MessageList.as_view(), name='conversation-senf'), 
    path('received/<int:pk>/', views.MessageReceived.as_view(), name='message-received'), 
    path('contacts/', views.ContactsListView.as_view(), name='user-list'), 
    path('api/conversations/<int:pk>/', views.ConversationDetailAPIView.as_view(), name='conversation-detail'),

    ]
