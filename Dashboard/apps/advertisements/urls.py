from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='adv_list'),
    
    
    # ///////////////// API خاص بالداشبورد //////////
    path('api/getaDvertisements/', views.AdvertisementListView.as_view(), name="get_advertisements"), #جلب بيانات الاعلانات
    path('api/createAdvertisement/', views.AdvertisementImageUploadView.as_view(), name="create_advertisement"), #إضافة إعلان   
    path('api/update/<int:pk>/', views.update_advertisement, name="update_advertisement"), #تعديل بيانات  إعلان
    path('api/delete/advertisement/<int:pk>/', views.delete_advertisement, name="delete_advertisement"), # حذف  إعلان
    
    
    
    # ////////////////////////////////////////////
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
