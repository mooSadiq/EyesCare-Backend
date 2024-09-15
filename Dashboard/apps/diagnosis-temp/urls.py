from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="diagnosis_list"),
    path('details', views.diagnosisDetails, name="diagnosis_details"),
    path('print',views.diagnosisDetailsPrint, name="diagnosis_Details_Print"),
    path('infer/', views.ImageInferenceView.as_view(), name='image-inference'),
    ]
