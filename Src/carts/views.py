from django.shortcuts import render, redirect
from .models import Cart
from product.models import BookList
from orders.models import Order
from accounts.forms import LoginForm, GuestRegisterForm
from billing.models import BillingProfile
from accounts.models import GuestEmail


# Create your views here.
def cart_home(request):
    template_name = 'carts/home.html'
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, template_name, {'cart': cart_obj})


def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            book_obj = BookList.objects.get_by_id(id=product_id)
        except BookList.DoesNotExist:
            return redirect('cart_home')
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if book_obj in cart_obj.books.all():
            cart_obj.books.remove(book_obj)
        else:
            cart_obj.books.add(book_obj)
        request.session['cart_items'] = cart_obj.books.count()
    return redirect('cart_home')


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.books.count() == 0:
        return redirect('cart_home')
    # else:
    #     order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
    user = request.user
    billing_profile_obj = None
    login_form = LoginForm()
    guest_register_form = GuestRegisterForm()
    guest_email_id = request.session.get('guest_email_id')
    if user.is_authenticated:
        # logged in user checkout ;
        billing_profile_obj, billing_profile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)
    elif guest_email_id is not None:
        # guest user checkout;
        guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
        billing_profile_obj, billing_profile_created = BillingProfile.objects.get_or_create(email=guest_email_obj.email)
    else:
        pass
    if billing_profile_obj is not None:
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile_obj, cart_obj)
        # if order_obj_created:
        #     del request.session['guest_email_id']

    context = {
        'object': order_obj,
        'login_form': login_form,
        'guest_register_form': guest_register_form,
        'billing_profile': billing_profile_obj
    }
    return render(request, 'carts/checkout.html', context)
