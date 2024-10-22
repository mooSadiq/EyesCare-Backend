from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
      
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)  
  
AUTH_PROVIDERS = {'email': 'email', 'google': 'google'}
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=10, choices=[('ذكر', 'ذكر'), ('أنثى', 'أنثى')], blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    user_type = models.CharField(max_length=20, choices=[('patient', 'مريض'), ('doctor', 'طبيب'), ('user', 'مستخدم عادي'), ('admin', 'ادمن'), ('support', 'فريق الدعم')])
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, null=True)
    verification_code_expiry = models.DateTimeField(null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_blue_verified = models.BooleanField(default=False)  # حقل شارة التوثيق الزرقاء
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
            
    auth_provider = models.CharField(max_length=50, blank=False, null=False, default=AUTH_PROVIDERS.get('email'))


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
      return f"{self.first_name} {self.last_name}"



class Address(models.Model):
    YEMEN_GOVERNORATES = [
        ('أبين', 'أبين'),
        ('عدن', 'عدن'),
        ('البيضاء', 'البيضاء'),
        ('الضالع', 'الضالع'),
        ('الحديدة', 'الحديدة'),
        ('الجوف', 'الجوف'),
        ('المهرة', 'المهرة'),
        ('المحويت', 'المحويت'),
        ('عمران', 'عمران'),
        ('ذمار', 'ذمار'),
        ('حضرموت', 'حضرموت'),
        ('حجة', 'حجة'),
        ('إب', 'إب'),
        ('لحج', 'لحج'),
        ('مأرب', 'مأرب'),
        ('ريمة', 'ريمة'),
        ('صعدة', 'صعدة'),
        ('صنعاء', 'صنعاء'),
        ('شبوة', 'شبوة'),
        ('سقطرى', 'سقطرى'),
        ('تعز', 'تعز'),
    ]    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_address')
    country = models.CharField(max_length=100, default="اليمن")
    governorate = models.CharField(max_length=100, null=True, choices=YEMEN_GOVERNORATES)
