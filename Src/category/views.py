from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Category
from product.models import BookList


# Create your views here.


class CategoryListView(ListView):
    template_name = 'category/list.html'
    paginate_by = 18

    def get_queryset(self, *args, **kwargs):
        return Category.objects.get_category()


class CategoryDetailsView(DetailView):
    template_name = 'category/details.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailsView, self).get_context_data(*args, **kwargs)
        books_obj = BookList.objects.get_by_category(self.object)
        context['object_list'] = books_obj
        return context

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        instance = Category.objects.get_by_slug(slug)
        if instance is None:
            raise Http404("Page not found")
        return instance
