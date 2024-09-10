from django.urls import path
from . import mobile_api

urlpatterns = [
    path('', mobile_api.PostListView.as_view(), name='post-list'),
    path('<int:pk>/', mobile_api.PostDetailView.as_view(), name='post-detail'),
    path('user/', mobile_api.UserPostsView.as_view(), name='user-posts'),
    path('create/', mobile_api.PostCreateView.as_view(), name='post-create'),
    path('like/<int:pk>/', mobile_api.LikePostView.as_view(), name='like-post'),
    path('delete/<int:pk>/', mobile_api.PostDeleteView.as_view(), name='post-delete'),
    path('update/<int:pk>/', mobile_api.PostUpdateView.as_view(), name='post-update'),
]
