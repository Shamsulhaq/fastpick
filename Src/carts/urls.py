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
from .views import cart_home, cart_add, cart_remove, checkout_home,success_view
    # ,shipping_method

urlpatterns = [
    path('', cart_home, name ='cart-home-url'),
    path('add/<id>', cart_add, name ='cart-add-url'),
    path('remove/<id>', cart_remove, name ='cart-remove-url'),
    path('checkout/', checkout_home, name ='checkout-home-url'),
    path('checkout/success/<id>', success_view, name ='success_view_url'),

]
