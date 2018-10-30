from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

from fastpick.utils import render_to_pdf
from orders.models import Order, OrderItem
from payment.models import RequestPayment
from .forms import RequestPaymentForm


# Create your views here.
def request_paymet_view(request, id):
    payment = RequestPayment.objects.get_by_order_id(id)
    if payment.status == 'unpaid':
        form = RequestPaymentForm(request.POST or None, instance=payment)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.order_id = payment.order_id
            instance.status = 'pending'
            instance.save()
            messages.success(request, 'Payment Submit Update Successfully')
        context = {
            "form": form,
            'payment': payment
        }
        return render(request, 'payment/paymrnt_request.html', context)
    elif payment.status == 'paid' or payment.status == 'pending':
        context = {
            'payment': payment
        }
        return render(request, 'payment/paymrnt_request.html', context)
    else:
        return redirect('book-list-view-url')


def print_invoice_view(request, id):
    order_obj = Order.objects.get_by_order_id(id)
    payment = RequestPayment.objects.get_by_order_id(id)
    order_items = OrderItem.objects.filter(order=order_obj)
    data = {
        'order_id': order_obj.order_id,
        'order_date': payment.update,
        'payment': payment.status,
        'name': order_obj.billing_profile.full_name,
        'email': order_obj.billing_profile.email,
        'phone':order_obj.billing_profile.phone,
        'order_items': order_items,
        'shipping': order_obj.shipping_total,
        'totla': order_obj.total,

    }
    pdf = render_to_pdf('mail/invoice.html', data)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"Invoice_{order_obj.order_id}.pdf"
        content = "inline; filename='%s'" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
