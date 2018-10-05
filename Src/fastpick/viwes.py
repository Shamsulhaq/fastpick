from django.views.generic import TemplateView, ListView
from product.models import BookList


class IndexView(TemplateView):
    template_name = 'index.html'


class SearchView(ListView):
    template_name = 'search/search_view.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SearchView, self).get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('q', None)
        if query is not None:
            return BookList.objects.search(query)
        else:
            return BookList.objects.is_stock()
