from django.contrib import admin
from payments.models import (PayYearsModel, TotalPriceModel, UserPriceModel, UserPaymentModel)

# Register your models here.
admin.site.register(PayYearsModel)
admin.site.register(UserPaymentModel)


@admin.register(TotalPriceModel)
class TotalPriceAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'price']


@admin.register(UserPriceModel)
class UserPriceAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_price', 'Installment', 'finished']
    raw_id_fields = ['user']
