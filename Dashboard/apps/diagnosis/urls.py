from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="diagnosis_list"),
    path('print',views.diagnosisDetailsPrint, name="diagnosis_Details_Print"),
    
    #//////// APIs for dashboard ///////////////
    path('api/report/page/<int:id>/', views.diagnosisDetails, name="diagnosis_details"), #رابط الانتقال الى صفحة التقرير
    # path('api/add_diagnose/', views.ImageUploadView.as_view(), name='add_diagnose'), #تشخيص صورة من الداش بورد
    # path('api/getDiagnosis/', views.DisagnosisListView.as_view(), name="get_Diagnosis"), # جلب بيانات التشخيصات
    # path('api/report/details/<int:pk>/', views.ReportDiagnosisView.as_view(), name="get_report"), # جلب بيانات التقرير
    # path('api/delete/<int:pk>/', views.DisagnosisListView.as_view(), name="delete_Diagnosis"), # جلب بيانات التقرير
    
    
]
