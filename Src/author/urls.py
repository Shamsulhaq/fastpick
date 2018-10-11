from django.urls import path
from .views import AuthorListView,AuthorDetailsView

urlpatterns = [
    path('list/',AuthorListView.as_view(),name ='author_list'),
    path('details/<slug>',AuthorDetailsView.as_view(),name ='author_details'),
]
