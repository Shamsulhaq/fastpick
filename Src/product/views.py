from django.shortcuts import render

from django.views.generic import ListView


#
# class GetIndex(ListView):
#     template_name = 'home.html'

def index(request):
    return render(request, 'index.html')


def home(request):
    return render(request, 'home.html')
