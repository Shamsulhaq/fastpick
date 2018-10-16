from django.shortcuts import render, redirect
from orders.models import Order


def dashboard_home(request):
    user = request.user
    print(user)
    order_obj = Order.objects.get_order_paid(user)
    title = 'Order Home'
    context = {

        'object': order_obj,
        'title':title
    }
    if user.is_authenticated:
        return render(request, 'dashboard/home.html', context)
    return redirect('get_login')


def dashboard_all(request):
    user = request.user
    order_obj = Order.objects.get_all_order(user)
    title = 'All Order'
    context = {
        'object': order_obj,
        'title':title
    }
    if user.is_authenticated:
        return render(request, 'dashboard/home.html', context)
    return redirect('get_login')


def dashboard_done(request):
    user = request.user
    order_obj = Order.objects.get_all_done(user)
    title = 'All Completed Order'
    context = {
        'object': order_obj,
        'title':title
    }
    if user.is_authenticated:
        return render(request, 'dashboard/home.html', context)
    return redirect('get_login')


def dashboard_pending(request):
    user = request.user
    order_obj = Order.objects.get_all_pending(user)
    title = 'All Pending Order'
    context = {
        'object': order_obj,
        'title':title
    }
    if user.is_authenticated:
        return render(request, 'dashboard/home.html', context)
    return redirect('get_login')


def dashboard_process(request):
    user = request.user
    order_obj = Order.objects.get_order_paid(user)
    title = 'All on Process Order or Paid'
    context = {
        'object': order_obj,
        'title':title
    }
    if user.is_authenticated:
        return render(request, 'dashboard/home.html', context)
    return redirect('get_login')


def order_info_view(request,id):
    user = request.user
    object = Order.objects.get(id=id)
    context = {
        'obj': object
    }
    if user.is_authenticated:
        return render(request, 'dashboard/home.html', context)
    return redirect('get_login')

