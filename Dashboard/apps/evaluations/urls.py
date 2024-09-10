from django.urls import path
from . import views
from . import api_mobile

urlpatterns = [
    # Dashboard urls
    path('', views.evaluations_page, name='evaluations_page'),
    path('mobileapi/getallreviews/',api_mobile.get_all_reviews,name='get_all_reviews'),
    path('mobileapi/deletereviews/<int:pk>/',api_mobile.delete_review,name='delete_review'),
    path('mobileapi/updatereview/<int:pk>/',api_mobile.update_review,name='update_review'),
    path('mobileapi/setreview/',api_mobile.set_review,name='set_review'),
    path('api/getreviews/',views.get_all_reviews,name='get_all_reviews_dashboard'),
    path('api/deletereview/<int:pk>/',views.delete_review,name='delete_review_dashboard'),
]

