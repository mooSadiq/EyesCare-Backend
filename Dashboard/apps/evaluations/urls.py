from django.urls import path
from . import views
from . import api_mobile

urlpatterns = [
    # Dashboard urls
    path('', views.evaluations_page, name='evaluations_page'),
    path('api/get/reviews/',views.get_all_reviews,name='get_all_reviews_dashboard'),
    path('api/delete/review/<int:pk>/',views.delete_review,name='delete_review_dashboard'),
]

