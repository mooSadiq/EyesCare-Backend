import os
from django import forms
from .models import doctors

class DoctorForm(forms.ModelForm):
  class Meta:
    model = doctors
    fields = ['name', 'phone', 'profile','photo', 'email', 'location', 'status']
    labels = {
      'name': 'الاسم:',
      'phone': 'رقم الهاتف:',
      'profile': 'الصورة:',
      'photo': 'الصورة2',
      'email': 'البريد الإلكتروني:',
      'location': 'الموقع:',
      'status': 'الحالة:',
    }
    widgets = {
      'name': forms.TextInput(attrs={'class': 'doc-form form-control', 'required': True}), 
      'phone': forms.NumberInput(attrs={'class': 'doc-form form-control', 'required': True}),
      'profile': forms.FileInput(attrs={'class': 'doc-form form-control'}),
      # 'photo': forms.ImageField(attrs={'class': 'doc-form form-control', 'required': True, 'accept': 'image/*'}),
      'email': forms.EmailInput(attrs={'class': 'doc-form form-control', 'required': True}),
      'location': forms.TextInput(attrs={'class': 'doc-form form-control', 'required': True}),
      'status' : forms.Select(choices=[('active', 'نشط'), ('inactive', 'غير نشط')], attrs={'class': 'doc-form form-control', 'required': True}),
    }
  def clean(self):
        cleaned_data = super().clean()
        if self.cleaned_data['photo']:
            photo = self.cleaned_data['photo']
            photo_name = f'doctors/_{photo.name}'  # Generate unique filename
            photo_path = os.path.join('media', photo_name)  # Path to save the image in media folder

            # Save the image to the project media directory
            with open(photo_path, 'wb') as f:
                f.write(photo.read())

            # Update the photo field with the new path
            cleaned_data['photo'] = photo_path

        return cleaned_data