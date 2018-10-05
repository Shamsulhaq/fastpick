from django.http import Http404

from django.views.generic import ListView, DetailView

from .models import BookList


class BookListView(ListView):
    template_name = 'book/list.html'
    paginate_by = 25

    def get_queryset(self, *args, **kwargs):
        return BookList.objects.all()


class BookDetailView(DetailView):
    template_name = 'book/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(BookDetailView, self).get_context_data(*args, **kwargs)
        context['title'] = '{}'.format(self.get_object().title)
        return context

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        instance = BookList.objects.get_by_slug(slug=slug)
        if instance is None:
            raise Http404("Page not found")
        return instance

