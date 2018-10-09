"""fastpick URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import login_page,register_page,guest_register_view

urlpatterns = [
    path('login', login_page, name='get_login'),
    path('guest', guest_register_view, name='guest_access'),
    path('logout', LogoutView.as_view(), name='get_logout'),
    path('register', register_page, name='get_register'),
]
