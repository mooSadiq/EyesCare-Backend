from django.contrib import admin
from django.urls import path
from . import views
from . import api_mobile


urlpatterns = [
path('', views.diseases_list, name="diseases_list"),
path('details/<int:pk>/', views.diseases_details, name="diseases_details"),
path('edit_details/<int:pk>/', views.edit_diseases_details, name="edit_diseases_details"),
path('api/get/diseases/',views.get_all_diseases,name="get_all_deseases"),
path('api/get/diseasebyid/<int:pk>/',views.get_disease_by_id,name="get_disease_by_id"),
path('api/get/diseasebyname/<str:name>/',views.get_all_diseases_byname,name="get_all_diseases_byname"),
path('api/set/disease/',views.set_diseas,name="set_diseas"),
path('api/update/disease/<int:pk>/',views.update_disease,name="upadate_disease"),
path('api/delate/disease/<str:pk>/',views.delete_diseases,name="delete_diseases"),
path('api/try/',views.try_diseases,name="delete_diseases"),
path('api/try/add/',views.DiseaseCreateView.as_view(),name="delete_diseases"),
path('api/try/get/',views.DiseaseTryListView.as_view(),name="delete_diseases"),
]