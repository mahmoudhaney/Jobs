from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

def send_message(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        email = request.POST['email']
        message = request.POST['message']

        send_mail(
            subject,
            message,
            email,
            [settings.EMAIL_HOST_USER],
        )
    return render(request, 'contact.html', {})