from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import AddressForm
from addresses.models import Address
from billing.models import BillingProfile
from orders.forms import ShippingMethodForm
# Create your views here.


def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)

    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        # print(request.POST)
        instance = form.save(commit=False)
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        if billing_profile:
            address_type = request.POST.get('address_type', 'shipping')
            instance.billing_profile = billing_profile
            instance.address_type = address_type
            instance.save()
            request.session[address_type + "_address_id"] = instance.id
            # print(address_type + "_address_id")
        else:
            print('ERROR!')
            return redirect('checkout-home-url')

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
    return redirect('checkout-home-url')


def shipping_method(request):
    form = ShippingMethodForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        instance = form.save(commit=False)
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        if billing_profile:
            shipping_method = request.POST.get('method', 'home delivery')
            instance.billing_profile = billing_profile
            instance.method = shipping_method
            instance.save()
            request.session['shipping_method_id'] = instance.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)


def checkout_address_reuse_view(request):
    if request.user.is_authenticated:
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if request.method == 'POST':
            # print(request.POST)
            shopping_address = request.POST.get('shopping_address', None)
            address_type = request.POST.get('address_type', 'shipping')
            billing_profile, created = BillingProfile.objects.new_or_get(request)
            if shopping_address is not None:
                qs = Address.objects.filter(billing_profile=billing_profile, id= shopping_address)
                if qs.exists():
                    request.session[address_type + "_address_id"] = shopping_address
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
    return redirect('checkout-home-url')



