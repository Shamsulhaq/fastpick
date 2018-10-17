from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from orders.models import Order
from billing.models import BillingProfile
from addresses.models import Address


@login_required
def dashboard(request):
    user = request.user
    billing_obj = get_object_or_404(BillingProfile,user=user, active= True)
    return render(request, 'dashboard/home.html', {'billing_obj': billing_obj})


@login_required
def on_process_order(request):
    user = request.user
    order_obj = Order.objects.get_order_paid(user)
    context = {

        'object': order_obj,
    }
    return render(request, 'dashboard/order.html', context)


@login_required
def all_order(request):
    user = request.user
    order_obj = Order.objects.get_all_order(user)
    context = {
        'object': order_obj,
    }
    return render(request, 'dashboard/order.html', context)


@login_required
def done_order(request):
    user = request.user
    order_obj = Order.objects.get_all_done(user)
    context = {
        'object': order_obj,
    }
    return render(request, 'dashboard/order.html', context)


@login_required
def pending_order(request):
    user = request.user
    order_obj = Order.objects.get_all_pending(user)
    context = {
        'object': order_obj,
    }
    return render(request, 'dashboard/order.html', context)


@login_required
def order_info_view(request, id):
    user = request.user
    object = Order.objects.get(id=id)
    context = {
        'obj': object
    }
    if user.is_authenticated:
        return render(request, 'dashboard/order.html', context)
    return redirect('get_login')


@login_required
def address_book(request):
    user = request.user
    billing_obj = get_object_or_404(BillingProfile,user=user, active= True)
    qs = Address.objects.filter(billing_profile=billing_obj, active=True)
    address_obj = qs
    return render(request,'dashboard/address_book.html', {'address_obj':address_obj})