from django.urls import path
from .views import ReviewListView

urlpatterns = [
    path('review/list/', ReviewListView.as_view(), name='review-list-view-url'),
]
