from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import LoginForm
from billing.models import BillingProfile
from product.models import BookList
from rent.models import RentCart, Rent


# Create your views here.


def rent_cart_home(request):
    template_name = 'rent/home.html'
    rent_cart_obj, new_obj = RentCart.objects.new_or_get(request)
    return render(request, template_name, {'rent_cart': rent_cart_obj})


def rent_cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            book_obj = BookList.objects.get_by_id(id=product_id)
        except BookList.DoesNotExist:
            return redirect('rent_cart_home_url')
        cart_obj, new_obj = RentCart.objects.new_or_get(request)
        if book_obj in cart_obj.books.all():
            cart_obj.books.remove(book_obj)
            request.session['rent_cart_items'] = cart_obj.books.count()  # to count cart items
            messages.warning(request, "Your are Rent Card item Removed!")
            return redirect('rent_cart_home_url')
        else:
            cart_obj.books.add(book_obj)
        request.session['rent_cart_items'] = cart_obj.books.count()
        messages.success(request, "Your are Rent Card item Added!")
    return redirect('rent_cart_home_url')


@login_required
def rent_checkout_home(request):
    cart_obj, cart_created = RentCart.objects.new_or_get(request)
    rent_obj = None
    if cart_created or cart_obj.books.count() == 0:
        return redirect('rent_cart_home_url')

    billing_profile, created = BillingProfile.objects.new_or_get(request)

    if billing_profile is not None:
        rent_obj, order_obj_created = Rent.objects.new_or_get(billing_profile, cart_obj)

    if request.method == 'POST':
        is_done = rent_obj.check_done()
        if is_done:
            rent_obj.mark_submit()
            request.session['rent_cart_items'] = 0
            del request.session['rent_id']
            return render(request, 'carts/success.html', {'object': rent_obj})
    context = {
        'object': rent_obj,

    }
    return render(request, 'rent/checkout.html', context)
