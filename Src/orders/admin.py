from django.contrib import admin
from .models import Order


# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'shipping_method', 'shipping_address', 'shipping_total', 'total',
                    'timestamp', 'update', 'active']
    search_fields = ['order_id__icontains', 'billing_profile__full_name']
    list_per_page = 20
    list_filter = ['shipping_method__method', 'timestamp', 'update', 'active']

    class Meta:
        Model = Order


admin.site.register(Order,OrderAdmin)
