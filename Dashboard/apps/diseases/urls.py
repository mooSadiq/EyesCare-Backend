from django.urls import path
from . import views



urlpatterns = [
path('', views.diseases_list, name="diseases_list"),
path('details/<int:pk>/', views.diseases_details, name="diseases_details"),
path('edit_details/<int:pk>/', views.edit_diseases_details, name="edit_diseases_details"),
path('api/get/diseases/',views.DiseasesList.as_view(),name="get_all_deseases"),
path('api/get/diseasebyid/<int:pk>/',views.DiseasList.as_view(),name="get_disease_by_id"),
path('api/get/all/diseasebyid/<int:pk>/',views.DiseasListall.as_view(),name="get_disease_by_id"),
path('api/set/disease/',views.DiseasesSet.as_view(),name="set_diseas"),
path('api/update/disease/<int:pk>/',views.DiseaseUpdate.as_view(),name="upadate_disease"),
path('api/delate/disease/<str:pk>/',views.DiseasesDelete.as_view(),name="delete_diseases"),
]