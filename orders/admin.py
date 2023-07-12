from django.contrib import admin
from orders.models import UserCart,UserOrders,UserOrderItems


admin.site.register(UserCart)
admin.site.register(UserOrders)
admin.site.register(UserOrderItems)
