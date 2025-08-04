# portfolio/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='portfolio/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),
    path('projects/', views.project_list, name='project_list'),
    path('certificates/', views.certificate_list, name='certificate_list'),
    path('cv/', views.cv, name='cv'),
]
