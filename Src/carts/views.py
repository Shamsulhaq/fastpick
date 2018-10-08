from django.shortcuts import render, redirect
from .models import Cart
from product.models import BookList


# Create your views here.
def cart_home(request):
    template_name = 'carts/home.html'
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, template_name, {'cart': cart_obj})


def cart_update(request):
    product_id = request.POST.get('product_id')
    book_obj = BookList.objects.get_by_id(id=product_id)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    if book_obj in cart_obj.books.all():
        cart_obj.books.remove(book_obj)
    else:
        cart_obj.books.add(book_obj)
    request.session['cart_items'] = cart_obj.books.count()
    return redirect('cart_home')
