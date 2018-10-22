from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from .models import Cart

from accounts.forms import LoginForm, GuestRegisterForm
from addresses.forms import AddressForm
from addresses.models import Address
from billing.models import BillingProfile
from product.models import BookList
from orders.models import Order, ShippingMethod
from orders.forms import ShippingMethodForm


# Create your views here.
def cart_home(request):
    template_name = 'carts/home.html'
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, template_name, {'cart': cart_obj})


def cart_update(request):
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    print(redirect_path)
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            book_obj = BookList.objects.get_by_id(id=product_id)
        except BookList.DoesNotExist:
            return redirect('cart-home-url')
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if book_obj in cart_obj.books.all():
            cart_obj.books.remove(book_obj)
            request.session['cart_items'] = cart_obj.books.count()  # to count cart items
            messages.warning(request, "Your are Card item Removed!")
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('cart-home-url')
        else:
            cart_obj.books.add(book_obj)
        request.session['cart_items'] = cart_obj.books.count()
        messages.success(request, "Your are Card item Added!")
    if is_safe_url(redirect_path, request.get_host()):
        return redirect(redirect_path)
    else:
        return redirect(book_obj.get_absolute_url())


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.books.count() == 0:
        return redirect('cart-home-url')

    login_form = LoginForm()
    guest_register_form = GuestRegisterForm()
    shipping_method_form = ShippingMethodForm()
    address_form = AddressForm()

    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)
    shipping_method_id = request.session.get("shipping_method_id", None)

    billing_profile, created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile, active=True)

        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)

        if shipping_method_id:
            order_obj.shipping_method = ShippingMethod.objects.get(id=shipping_method_id)
            del request.session["shipping_method_id"]

        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]

        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
            if shipping_address_id:
                del request.session["shipping_address_id"]

        if shipping_method_id or billing_address_id or shipping_address_id:
            order_obj.save()

    if request.method == 'POST':
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_submit()
            request.session['cart_items'] = 0
            del request.session['cart_id']
            if not request.user.is_authenticated:
                del request.session['guest_email_id']
            return render(request, 'carts/success.html', {'object': order_obj})
    context = {
        'object': order_obj,
        'login_form': login_form,
        'guest_register_form': guest_register_form,
        'billing_profile': billing_profile,
        'address_form': address_form,
        'address_qs': address_qs,
        'shipping_method_form': shipping_method_form,

    }
    return render(request, 'carts/checkout.html', context)

# def cart_success_view(request):
#     return render(request, 'carts/success.html')
