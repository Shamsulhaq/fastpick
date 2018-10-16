from django.urls import path
from .views import dashboard_home,dashboard_all,order_info_view,dashboard_done,dashboard_pending,dashboard_process

urlpatterns = [
    path('home/', dashboard_home, name='dashboard_home'),
    path('all/', dashboard_all, name='dashboard_all'),
    path('pending/', dashboard_pending, name='dashboard_pending'),
    path('paid/', dashboard_process, name='dashboard_process'),
    path('done/', dashboard_done, name='dashboard_done'),
    path('order_info/<id>', order_info_view, name='order_info_url'),
]