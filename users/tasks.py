from celery import shared_task
from django.core.mail import send_mail,EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from twilio.rest import Client


@shared_task(bind = True)
def displayNumberFunction(self,a,b):
    print(self)
    for i in range(10):
        print(i)
    print(a+b)
    return 'printed from 1 to 10'


@shared_task(bind = True)
def order_mail(self,email,name,item,total,house,street,city,state,pincode):
    try:
        context = {
            'name' : name,
            'item' : item,
            'total' : total,
            'house' : house,
            'street' : street,
            'city' : city,
            'state' : state,
            'pincode' : pincode,
        }
        template = 'orders/order_email_template.html'
        html_content = render_to_string(template,context)
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


@shared_task(bind = True)
def password_reset_mail(self,email,token,name):
    try:
        context = {
            'token' : token,
            'user' : name ,
        }
        template = 'users/forgot_password_email_template.html'
        html_content = render_to_string(template,context)
        subject="Reset Password Mail"

        email = EmailMessage(subject,html_content,to=[email])
        email.content_subtype = 'html'
        email.send()

        return f'mail sent successfully'
    except Exception as e:
        print(str(e))


@shared_task(bind = True)
def order_status_mail(self,email,status,items,user):
    try:
        context = {
            'status' : status,
            'items' : items,
            'user' : user,
        }
        template = 'orders/order_status_email_template.html'
        html_content = render_to_string(template,context)
        subject="Your Order Status"

        email = EmailMessage(subject,html_content,to=[email])
        email.content_subtype = 'html'
        email.send()

        return f'mail sent successfully'
    except Exception as e:
        print(str(e))


@shared_task(bind = True)
def send_sms(self,to_number, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    twilio_phone_number = settings.TWILIO_PHONE_NUMBER

    client.messages.create(
        to=to_number,
        from_=twilio_phone_number,
        body=message
    )

    return f"SMS sent successfully !"