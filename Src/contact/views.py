from django.shortcuts import render,redirect
from django.contrib.messages.views import messages
from .forms import ContactForm
from .models import Contact

# Create your views here.


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    template_name = 'contact/contact.html'
    context = {
        "form": contact_form
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        Contact.objects.create(name=name, phone=phone, email=email, subject=subject, message=message)
        messages.success(request, "Your Message send successful")

    return render(request, template_name, context)