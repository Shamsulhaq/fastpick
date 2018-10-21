from django.urls import path
from .views import ReviewListView,ReviewDetailView

urlpatterns = [
    path('review/list/', ReviewListView.as_view(), name='review-list-view-url'),
    path('review/detail/<slug>', ReviewDetailView.as_view(), name='review-detail-view-url'),
]
