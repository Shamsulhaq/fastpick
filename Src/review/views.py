from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from review.models import Review


class ReviewListView(ListView):
    template_name = 'review/home.html'
    paginate_by = 25

    def get_queryset(self, *args, **kwargs):
        return Review.objects.all()