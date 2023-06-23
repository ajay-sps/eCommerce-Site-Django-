from django.core.mail import send_mail
from django.conf import settings


def verification_mail(token,email):

    subject = 'Email Verification'
    message = f"please click on the link to verify your account http://127.0.0.1:8000/user/verification/{token}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject,message,from_email,recipient_list)