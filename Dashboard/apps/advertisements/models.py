
from django.db import models
from apps.users.models import CustomUser
# Create your models here.
class Advertisement(models.Model):
    advertiser = models.CharField(max_length=255)  # اسم الجهة المعلنة
    ad_image = models.ImageField(upload_to='ads/', blank=True, null=True)  # صورة الإعلان   
    ad_link = models.CharField(max_length=200)  # رابط يتم توجيه المستخدم إليه عند النقر على الإعلان
    phone_number = models.CharField(max_length=15)  # رقم هاتف الجهة المعلنة
    start_date = models.DateField()  # تاريخ بدء عرض الإعلان
    end_date = models.DateField()  # تاريخ انتهاء عرض الإعلان
    status = models.IntegerField( default=1)  # الحالة لتحديد إذا كان الإعلان نشطاً أو لا 0 قيد الانتظار و1 نشط و2 منتهي
    about = models.CharField(max_length=800) # نص الاعلان 
    views_count = models.PositiveIntegerField(default=0)  # عدد مرات مشاهدة الإعلان
    clicks_count = models.PositiveIntegerField(default=0)  #  عدد مرات النقر على الإعلان
    allowed = models.BooleanField(default=True) # مسموح بالعرض او موقف مثل حظر المنشور
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.advertiser},{self.status},{self.views_count},{self.clicks_count}"