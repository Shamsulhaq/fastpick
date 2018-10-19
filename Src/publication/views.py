from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Publication
from product.models import BookList


# Create your views here.


class PublicationListView(ListView):
    template_name = 'publication/list.html'
    paginate_by = 18

    def get_queryset(self, *args, **kwargs):
        return Publication.objects.get_publication()


class PublicationDetailsView(DetailView):
    template_name = 'publication/details.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PublicationDetailsView, self).get_context_data(*args, **kwargs)
        books_obj = BookList.objects.get_by_publication(self.object)
        context['object_list'] = books_obj
        return context

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        instance = Publication.objects.get_by_slug(slug)
        print(instance)
        if instance is None:
            raise Http404("Page not found")
        return instance
