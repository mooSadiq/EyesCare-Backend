from django.urls import path
from . import views
from . import mobile_api
urlpatterns = [
    path('', views.chatview, name="chat_list"),
    path('api/get/users/', views.UsersListView.as_view(), name='users-list'),
    path('api/get/conv/', mobile_api.ConversationList.as_view(), name='conv-list'),
    path('received/<int:pk>/', views.MessageReceived.as_view(), name='message-received'), 
    path('contacts/', views.ContactsListView.as_view(), name='user-list'), 

    ]
