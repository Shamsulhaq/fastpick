from django.urls import path
from .views import PublicationListView, PublicationDetailsView

urlpatterns = [
    path('list/', PublicationListView.as_view(), name='publication_list_view_url'),
    path('details/<slug>', PublicationDetailsView.as_view(), name='publication_details_view_url'),
]
