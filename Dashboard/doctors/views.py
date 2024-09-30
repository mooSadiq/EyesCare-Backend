from django.shortcuts import redirect, render
from .models import doctors
from .forms import DoctorForm

# Create your views here.

def index(request):
    all_doctors = doctors.objects.all
    return render(request, 'index.html',{'doctors':all_doctors})



def add_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            new_doctor = form.save() # Save the doctor model
            # Update the photo field with the generated path
            new_doctor.photo = form.cleaned_data['photo']
            new_doctor.save()  # Save the updated model
            return redirect('doc-index') # Redirect to your doctors list view after successful save
    else:
        form = DoctorForm()
        return render(request, 'add_doctor.html', {'form': form})


# def add_doctor(request):
    
    
#     return render(request, 'add_doctor.html')