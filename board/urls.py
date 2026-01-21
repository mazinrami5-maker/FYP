# board/urls.py
from django.urls import path
from . import views
from django.urls import re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('projecthub/', views.projecthub, name='projecthub'),
    path('logout/', views.logout_view, name='logout'),

    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]
