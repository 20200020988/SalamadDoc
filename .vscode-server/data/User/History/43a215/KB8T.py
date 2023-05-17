from django.shortcuts import render

# Create your views here.
def home (request):
    return render(request, 'home.html', {})

def contact (request):
    if request.method == "POST":
        patient_name
        patient_email
        patient_subject
        patient_message
    else:
        return render(request, 'contact.html', {})