from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import BookAuthor
from product.models import BookList


# Create your views here.


class AuthorListView(ListView):
    template_name = 'author/list.html'
    paginate_by = 20

    def get_queryset(self, *args, **kwargs):
        return BookAuthor.objects.get_authors()


class AuthorDetailsView(DetailView):
    template_name = 'author/details.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AuthorDetailsView, self).get_context_data(*args, **kwargs)
        books_obj = BookList.objects.get_by_author(self.object)
        context['object_list'] = books_obj
        return context

    def get_object(self, *args, **kwargs):
        instance = None
        slug = self.kwargs.get('slug')
        qs = BookAuthor.objects.filter(slug=slug)
        if qs.count() == 1:
            instance = qs.first()
        if instance is None:
            raise Http404("Page not found")
        return instance
