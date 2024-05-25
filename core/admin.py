from django.contrib import admin
from core.models import ContactUs, Comment

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'topic', 'timestamp']