from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.messages.views import messages
from django.utils.http import is_safe_url

from .forms import LoginForm, RegisterForm, GuestRegisterForm
from .models import GuestEmail

User = get_user_model()


# Create your views here.
def guest_register_view(request):
    form = GuestRegisterForm(request.POST or None)
    template_name = 'accounts/login.html'
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get("email")
        phone = form.cleaned_data.get("phone")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        request.session['guest_phone'] = phone
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('get_register')
    return redirect('get_register')


def login_page(request):
    form = LoginForm(request.POST or None)
    template_name = 'accounts/login.html'
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
                print("del session guest email")
            except:
                pass
                print("Error del session guest email")

            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('list')
        else:
            print("ERROR")
    return render(request, template_name, context)


def register_page(request):
    form = RegisterForm(request.POST or None)
    template_name = 'accounts/register.html'
    context = {
        "form": form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        new_user = User.objects.create_user(username, email, password)
        print(new_user)
        messages.success(request, "Your are registered!")
        return redirect('get_login')
    return render(request, template_name, context)
