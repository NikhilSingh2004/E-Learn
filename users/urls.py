from django.urls import path
from users import views

urlpatterns = [
    path('', views.UserHome, name='UserHome'),
    path('delete/', views.DeleteUser, name='DeleteUser'),
    path('edit/<str:username>/', views.EditUser, name="EditProfile"),
]
