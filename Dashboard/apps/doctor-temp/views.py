from django.shortcuts import render

# Create your views here.
def doctors_list(request):
    return render(request, 'doctors_list.html')

def userProfile(request):
  return render(request, 'doctor_profile.html')
