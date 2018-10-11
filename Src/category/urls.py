from django.urls import path
from .views import CategoryListView,CategoryDetailsView

urlpatterns = [
    path('list/',CategoryListView.as_view(),name ='category_list'),
    path('details/<slug>',CategoryDetailsView.as_view(),name ='category_details'),
]
