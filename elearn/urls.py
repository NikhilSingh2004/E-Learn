from elearn import views
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "E-Learn Website Dashboard"
admin.site.site_title = "E-Learn"
admin.site.index_title = "Welcome to E-Learn Site Aministration, Only for Admenistrative Purposes!"

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls')),
    path('user/', include('users.urls')),
    path('<str:anything>/', views.PageNotFound, name='PageNotFound') # Design the 404 Page 
]
