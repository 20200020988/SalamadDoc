from django.shortcuts import render
from django.core.mail import send_mail

# Create your views here.
def home (request):
    return render(request, 'home.html', {})

def contact(request):
    if request.method == "POST":
        patient_name = request.POST['patient_name']
        patient_email = request.POST['patient_email']
        patient_subject = request.POST['patient_subject']
        patient_message = request.POST['patient_message']

        send_mail(
            patient_subject,  # Subject
            patient_message,  # Message
            patient_email,    # Sender's email
            ['kylenabo45@gmail.com'],  # Recipient's email(s)
        )
        
    else:
        return render(request, 'contact.html', {})