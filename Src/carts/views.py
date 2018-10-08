from django.shortcuts import render
from .models import Cart


# Create your views here.
def cart_home(request):
    template_name = 'carts/home.html'
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request,template_name, {})


