from django.http import Http404

from django.views.generic import ListView, DetailView

from rent.models import RentCart
from .models import BookList
from carts.forms import CartAddProductForm
from orders.models import OrderItem


class BookListView(ListView):
    template_name = 'book/list.html'
    paginate_by = 20

    def get_context_data(self, *args, **kwargs):
        context = super(BookListView, self).get_context_data(*args, **kwargs)
        context['cart_product_form'] = CartAddProductForm()
        return context

    def get_queryset(self, *args, **kwargs):
        return BookList.objects.all()


class BookDetailView(DetailView):
    template_name = 'book/detail.html'

    def get_context_data(self, *args, **kwargs):

        context = super(BookDetailView, self).get_context_data(*args, **kwargs)
        context['title'] = '{}'.format(self.get_object().title)
        rent_cart_obj, new_obj = RentCart.objects.new_or_get(self.request)
        context['rent_cart'] = rent_cart_obj
        context['cart_product_form'] = CartAddProductForm()
        return context

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        instance = BookList.objects.get_by_slug(slug=slug)
        if instance is None:
            raise Http404("Page not found")
        return instance

