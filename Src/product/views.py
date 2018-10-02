from django.shortcuts import render

from django.views.generic import ListView

from .models import BookList


class Book_List_Viwe(ListView):
    template_name = 'book/booklist.html'
    model = BookList
