from django.contrib.messages.views import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order


@login_required
def index(request):
    if request.user.is_staff:
        order_obj = Order.objects.all()
        context = {
            'object': order_obj
        }
        return render(request, 'order-manager/index.html', context)
    return redirect('dashboard_home')


@login_required
def done_order(request):
    if request.user.is_staff:
        order_obj = Order.objects.filter(status='shipped')
        context = {
            'object': order_obj
        }
        return render(request, 'order-manager/index.html', context)
    return redirect('dashboard_home')


@login_required
def on_process_order(request):
    if request.user.is_staff:
        order_obj = Order.objects.filter(status='paid')
        context = {
            'object': order_obj
        }
        return render(request, 'order-manager/index.html', context)
    return redirect('dashboard_home')


@login_required
def pending_order(request):
    if request.user.is_staff:
        order_obj = Order.objects.filter(status='submit')
        context = {
            'object': order_obj
        }
        return render(request, 'order-manager/index.html', context)
    return redirect('dashboard_home')


@login_required
def single_order(request, id):
    if request.user.is_staff:
        object = Order.objects.get(id=id)
        context = {
            'obj': object
        }
        return render(request,'order-manager/single_order.html',context)
    return redirect('dashboard_home')