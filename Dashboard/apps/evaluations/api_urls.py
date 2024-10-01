
from django.urls import path
from . import api_mobile

urlpatterns = [
    path('get/reviews/',api_mobile.ReviewsListView.as_view(),name='get_all_reviews'),
    path('delete/<int:pk>/',api_mobile.DeleteReviewView.as_view(),name='delete_review'),
    path('update/<int:pk>/',api_mobile.UpdateReviewView.as_view(),name='update_review'),
    path('set/',api_mobile.SetReviewsView.as_view(),name='set_review'),
]