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


# @shared_task(bind = True)
def order_mail(email,name,total,house,street,city,state,pincode,items):
    try:
        context = {
            'name' : name,
            'total' : total,
            'house' : house,
            'street' : street,
            'city' : city,
            'state' : state,
            'pincode' : pincode,
            'items' : items
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


# @shared_task(bind = True)
def verification_mail(token,email,name,url):
    try:
        print(email,token,name,url)
        context = {
            'token' : token,
            'name' : name ,
            'url' : url,
        }
        subject = 'Email Verification'
        template = 'users/email_verification_email_template.html'
        html_content = render_to_string(template,context)

        email = EmailMessage(subject,html_content,to=[email])
        email.content_subtype = 'html'
        email.send()
        
        return f'mail sent successfully'
    except Exception as e:
        print(str(e))


# @shared_task(bind = True)
def password_reset_mail(email,token,name,url):
    try:
        print(email,token,name,url)
        context = {
            'token' : token,
            'user' : name ,
            'url' : url,
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


# @shared_task(bind = True)
def order_status_mail(email,status,items,user):
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


# @shared_task(bind = True)
def send_sms(to_number, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    twilio_phone_number = settings.TWILIO_PHONE_NUMBER
    
    client.messages.create(
        to = to_number,
        from_ = twilio_phone_number,
        body = message
    )

    return f"SMS sent successfully !"