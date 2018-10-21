from django.http import Http404
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView,DetailView

from review.models import Review


class ReviewListView(ListView):
    template_name = 'review/home.html'
    paginate_by = 25

    def get_queryset(self, *args, **kwargs):
        return Review.objects.all()


class ReviewDetailView(DetailView):
    template_name = 'review/detail_view.html'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        instance = Review.objects.get_by_slug(slug=slug)
        if instance is None:
            raise Http404("Page not found")
        return instance