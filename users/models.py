from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import AbstractUser
from products.models import ProductVariants
import secrets
from django.db.models.signals import pre_save
from django.dispatch import receiver

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
    profile_image = models.ImageField(upload_to='users/profile_images',default='users/profile_images/default.jpeg')
    token = models.CharField(max_length=16,unique=True,null=True)


    def __str__(self) -> str:
        return self.user.first_name + self.user.last_name
    
    def generate_token(self):
        self.token = secrets.token_hex(8) 
        self.save()


class SellerInventory(BaseModel):

    seller = models.ForeignKey(User,on_delete=models.PROTECT,related_name='seller_inventory')
    product_variant = models.ForeignKey(ProductVariants,on_delete= models.PROTECT,related_name='seller_inventory')
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return self.product_variant.code
    

class UserAddress(BaseModel):

    user = models.ForeignKey(User,on_delete=models.PROTECT,related_name='address')
    house_no = models.CharField(max_length=20,default=120)
    street = models.CharField(max_length=30,default= 'st 1220.')
    city = models.CharField(max_length=50,default='bhiwani') 
    state = models.CharField(max_length=40,default='haryana')
    postal_code = models.CharField(max_length=40,default=127028)
    detail_address = models.CharField(max_length=255,blank=True,null=True)


@receiver(pre_save,sender = UserAddress)
def update_detail_address(sender,instance,**kwargs):
    instance.detail_address = ", ".join(filter(None,[instance.house_no,instance.street,instance.city,instance.state,instance.postal_code]))