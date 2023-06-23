from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import AbstractUser
import secrets


class Roles(BaseModel):

    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class User(BaseModel,AbstractUser):

    role = models.ForeignKey(Roles,on_delete = models.PROTECT,related_name='user',default=None,null=True)
    is_verified = models.BooleanField(default=False)


class UserProfile(BaseModel):

    user = models.OneToOneField(User,on_delete=models.PROTECT,related_name='profile')
    contact = models.CharField(max_length=16)
    city = models.CharField(max_length=40)
    state = models.CharField(max_length=40)
    pincode = models.CharField(max_length=12)
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120,null=True,blank=True)
    profile_image = models.ImageField(upload_to='users/profile_images')
    token = models.CharField(max_length=16,unique=True,null=True)


    def __str__(self) -> str:
        return self.user.first_name + self.user.last_name
    
    def generate_token(self):
        self.token = secrets.token_hex(8) 
        self.save()
