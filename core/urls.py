from django.urls import path
from core import views

urlpatterns = [
    path('', views.Home, name='Home'),
    path('login/', views.LogIn, name='LogIn'),
    path('about/', views.About, name='About'),
    path('logout/', views.LogOut, name='LogOut'),
    path('signup/', views.SignUp, name='SignUp'),
    path('contact/', views.Contact, name='Contact'),
    path('change/', views.ChangePassword, name='ChangePassword'),

    path('sendMail/', views.SendMail, name='SendMail')

    # Forget Password Missing!
]
