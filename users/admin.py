from django.contrib import admin
from users.models import User,UserProfile,Roles,SellerInventory


admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Roles)
admin.site.register(SellerInventory)
