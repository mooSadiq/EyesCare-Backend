from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_verified', 'is_blue_verified')
    ordering = ('email',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'user_type', 'is_blue_verified')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'gender', 'birth_date', 'profile_picture', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'is_blue_verified')}),
        ('User Type', {'fields': ('user_type',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)