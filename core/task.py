# myapp/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactUs

@shared_task
def send_contact_email(subject, body, email):
    try:
        send_mail(subject, body, email, [settings.EMAIL_HOST_USER])
        return True
    except Exception as e:
        print(e)
        return False

# myapp/tasks.py
from celery import shared_task

@shared_task
def test_celery():
    return 'Celery is working!'
