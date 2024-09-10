from django.urls import path
from . import mobile_api
from . import views


urlpatterns = [
    path('',views.index, name='posts_list'),
    path('details/', views.postDetails, name='post_details'),
    
    path('api/get/posts/', views.PostListView.as_view(), name='post-list'),
    path('api/create/', mobile_api.PostCreateView.as_view(), name='post-create'),
    path('api/delete/<int:pk>/', mobile_api.PostDeleteView.as_view(), name='post-delete'),



]
