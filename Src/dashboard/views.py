from django.shortcuts import render, redirect


def dashboard_home(request):
    if request.user.is_authenticate:
        return render(request, 'dashboard/home.html')
    return redirect('get_login')
