from django.contrib import admin
from users.models import User,UserProfile,Roles,SellerInventory,UserAddress


admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Roles)
admin.site.register(SellerInventory)
admin.site.register(UserAddress)
