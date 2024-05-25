from django.urls import path
from courses import views

urlpatterns = [
    path('', views.CoursesHome, name='CoursesHome'),

    # Topic Home For Reply Comment!
    path('<str:name>/<int:topic>/<int:comment>/', views.TopicHome, name='TopicHome'),
    path('<int:topic>/<int:comment>/', views.ReplyComment, name='ReplyComment'),

    # Topic Home for Post Comment!
    path('<str:name>/<int:topic>/', views.TopicHome, name='TopicHome'),
    path('<int:topic>/', views.PostComment, name='PostComment'),

    # Default Topic Home
    path('<str:name>/', views.TopicHome, name='TopicHome'),

]
