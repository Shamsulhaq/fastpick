from django.urls import path
from .views import AuthorListView, AuthorDetailsView

urlpatterns = [
    path('list/', AuthorListView.as_view(), name='author-list-url'),
    path('details/<slug>', AuthorDetailsView.as_view(), name='author-details-url'),
]
