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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .viwes import IndexView,SearchView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls, name ='admin'),
    path('', include('accounts.urls')),
    path('', include('order-manager.urls')),
    path('', include('dashboard.urls')),
    path('', include('addresses.urls')),
    path('', include('review.urls')),
    path('accounts/', include('accounts.password.urls')),
    path('author/', include('author.urls')),
    path('book/', include('product.urls')),
    path('cart/', include('carts.urls')),
    path('category/', include('category.urls')),
    path('contact/', include('contact.urls')),
    path('publication/', include('publication.urls')),
    path('search/', SearchView.as_view(), name='search'),
    path('tinymce/',include('tinymce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
