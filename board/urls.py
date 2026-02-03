# board/urls.py
from django.urls import path
from . import views
from django.urls import re_path
from django.views.generic import TemplateView
from django.urls import path
from .views import create_project

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('projecthub/', views.projecthub, name='projecthub'),
    path('logout/', views.logout_view, name='logout'),
    path('projects/create/', create_project, name='create_project'),
    path('kanban/<int:project_id>/', views.kanban, name='kanban'),
    path('kanban/<int:project_id>/add_task/', views.add_task, name='add_task'),
    path('kanban/<int:project_id>/move_task/', views.move_task, name='move_task'),
    
    path("kanban/<int:project_id>/delete_task/",views.delete_task,name="delete_task"),
    
    path("kanban/<int:project_id>/update_task/", views.update_task_name, name='update_task_name'),
path("kanban/task/<int:task_id>/update/", views.update_task_details, name='update_task_details'),






    




  
    


]
