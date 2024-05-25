from django import forms
from .models import ContactUs
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

# Form for User Sign Up
class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password...'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password...'})
    )

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

# Form for User LogIn
class AuthenticateUserForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User Name...'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password...'})
    )

# Form For Changing Password
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password...'}),
        label='Old Password',
        strip=False,
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password...'}),
        label='New Password',
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password...'}),
        label='Confirm Password',
        strip=False,
    )

# Form For Contact Us
class FormContactUs(forms.ModelForm):
    class Meta:

        model = ContactUs

        fields = ['first_name', 'last_name', 'username', 'email', 'subject', 'body', 'footer']

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
                'placeholder': 'User Name...(Optional)'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Email...'
            }),
            'subject' : forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Purpose of this Mail...'
            }),
            'body' : forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Mail Body : Hello this is XYZ...'
            }),
            'footer' : forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Footer Note...(Optional)'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make username field optional
        self.fields['username'].required = False