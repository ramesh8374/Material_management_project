from django.core.mail import send_mail
from django.conf import settings

def send_email_to_user(vendor_email, subject, body):
    try:
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject, body, email_from, [vendor_email])
    except Exception as e:
        print(e)