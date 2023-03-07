from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name="Home"),
    path('add_task', views.Add_Task, name="Add Task"),
    path('login/', views.Login, name="Login"),
    path('logout/', views.Logout, name="Logout"),
    path('register/', views.register, name="Register"),
    path('remove_task/<int:task_id>/', views.Remove_Task, name='Remove Task'),
]
