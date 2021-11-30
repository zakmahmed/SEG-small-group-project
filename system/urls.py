"""system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from clubs import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign_up/', views.sign_up, name = 'sign_up'),
    path('create_club/', views.create_club, name = 'create_club'),
    path('', views.home, name= 'home'),
    path('user_home/', views.user_home, name= 'user_home'),
    path('log_in/', views.log_in, name='log_in'),
    path('club_list/', views.club_list, name='club_list'),
    path('club_profile/<club_name>/', views.club_profile, name ='club_profile'),
    path('view_members/<club_name>/', views.view_members, name ='view_members')
]
