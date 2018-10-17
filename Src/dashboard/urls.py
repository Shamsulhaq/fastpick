from django.urls import path
from .views import dashboard, on_process_order, all_order, order_info_view, done_order, pending_order, address_book

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard_home'),
    path('dashboard/address/', address_book, name='address_book_url'),
    path('dashboard/on_process/order/', on_process_order, name='on_process_order'),
    path('dashboard/all/order/', all_order, name='dashboard_all_order'),
    path('dashboard/pending/order/', pending_order, name='dashboard_pending'),
    path('dashboard/done/order/', done_order, name='dashboard_done'),
    path('dashboard/order_info/<id>', order_info_view, name='order_info_url'),
]
