from django.urls import path
from .views import dashboard, account_info, on_process_order, all_order, order_info_view, done_order, pending_order, \
    address_book, all_rent, rent_info_view, done_rent, pending_rent,return_rent

urlpatterns = [
    path('db/', dashboard, name='dashboard_home'),
    path('db/account/', account_info, name='db-account-url'),
    path('db/address/', address_book, name='db-address-book-url'),
    path('order/on-process', on_process_order, name='on-process-order-view-url'),
    path('order/all/', all_order, name='all-order-view-url'),
    path('order/pending/', pending_order, name='pending-order-view-url'),
    path('order/done/', done_order, name='done-order-view-url'),
    path('order/order_info/<id>', order_info_view, name='order-info-view-url'),
    path('rent/all/', all_rent, name='all-rent-view-url'),
    path('rent/rent_info/<id>', rent_info_view, name='rent-info-view-url'),
    path('rent/pending/', pending_rent, name='pending-rent-view-url'),
    path('rent/done/', done_rent, name='done-rent-view-url'),
    path('rent/return/', return_rent, name='return-rent-view-url'),
]
