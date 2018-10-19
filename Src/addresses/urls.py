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
from .views import checkout_address_create_view,checkout_address_reuse_view,shipping_method
urlpatterns = [
    path('address/create/', checkout_address_create_view, name='address-create-url'),
    path('address/reuse/', checkout_address_reuse_view, name='address-reuse-url'),
    path('shipping/method/', shipping_method, name ='shipping-method-url'),
]
