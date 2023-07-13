from celery import shared_task
from django.core.mail import send_mail,EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


@shared_task(bind = True)
def displayNumberFunction(self,a,b):
    print(self)
    for i in range(10):
        print(i)
    print(a+b)
    return 'printed from 1 to 10'


@shared_task(bind = True)
def order_mail(self,email):
    try:
        print(self)
        template = 'orders/order_email_template.html'
        html_content = render_to_string(template)
        subject="Order Confirmation Mail"

        email = EmailMessage(subject,html_content,to=[email])
        email.content_subtype = 'html'
        email.send()

        return f'mail sent successfully'
    except Exception as e:
        print(str(e))


@shared_task(bind = True)
def verification_mail(self,token,email):
    try:
        subject = 'Email Verification'
        message = f"please click on the link to verify your account http://127.0.0.1:8000/user/verification/{token}"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        send_mail(subject,message,from_email,recipient_list)
        return f'mail sent successfully'
    except Exception as e:
        print(str(e))
