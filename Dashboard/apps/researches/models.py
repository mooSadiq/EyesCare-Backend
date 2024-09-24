from django.db import models
from apps.users.models import CustomUser

# Create your models here.

class Field(models.Model):
    name = models.CharField(max_length=100)  # اسم المجال
    created_at = models.DateField(auto_now_add=True)  

    def __str__(self):
        return self.name


class Journal(models.Model):
    name = models.CharField(max_length=255)  
    website_url = models.URLField()  # رابط موقع المجلة
    created_at = models.DateField(auto_now_add=True)  

    def __str__(self):
        return self.name


class Research(models.Model):
    title = models.CharField(max_length=255) 
    abstract = models.TextField()  
    publication_date = models.DateField()  # تاريخ النشر
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)  # معرف المجلة التي نُشر فيها البحث
    authors = models.CharField(max_length=255)  
    institution = models.CharField(max_length=255) 
    pdf_file = models.FileField(upload_to='pdfs/')  # ملف PDF
    field = models.ForeignKey(Field, on_delete=models.CASCADE)  # معرف المجال (التصنيف العلمي)
    views_count = models.PositiveIntegerField(default=0)  # عدد مرات مشاهدة البحث
    downloads_count = models.PositiveIntegerField(default=0)  # عدد مرات تحميل البحث
    created_at = models.DateField(auto_now_add=True)  
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 

    def __str__(self):
        return self.title