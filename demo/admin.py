from django.contrib import admin

from demo.forms import OrderAdminForm
from demo.models import *


class ItemInOrder(admin.TabularInline):
    model = OrderInItem


class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm
    list_filter = ('status',)
    list_display = ('date', 'user',)
    fields = ('status', 'reject_reason')
    inlines = (ItemInOrder,)


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(User)
