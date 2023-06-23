from django.contrib import admin
from users.models import User,UserProfile,Roles


admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Roles)

# Register your models here.
