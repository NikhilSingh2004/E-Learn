from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

# Form for Edit Profile
class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'First Name...'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Last Name...'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'User Name...'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Email...'
            })
        }

        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
        }

        help_texts = {
            'username': 'An unique username.',
            'email': 'Enter a valid email address.',
        }


