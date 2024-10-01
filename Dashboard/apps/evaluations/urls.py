from django.urls import path
from . import views


urlpatterns = [
    # Dashboard urls
    path('', views.evaluations_page, name='evaluations_page'),
    path('api/get/reviews/',views.ReviewsListView.as_view(),name='get_all_reviews_dashboard'),
    path('api/delete/review/<int:pk>/',views.DeleteReviewView.as_view(),name='delete_review_dashboard'),
]

