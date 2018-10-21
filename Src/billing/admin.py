from django.contrib import admin
from .models import BillingProfile


# Register your models here.
class BillingProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'email']
    search_fields = ['full_name', 'email']
    list_filter = ['active', 'verify']

    class Meta:
        Model = BillingProfile


admin.site.register(BillingProfile, BillingProfileAdmin)
