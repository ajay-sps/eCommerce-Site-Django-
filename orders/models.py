from django.db import models
from base.models import BaseModel
from users.models import User,UserAddress
from products.models import ProductVariants



class UserCart(BaseModel):

    user = models.ForeignKey(User,on_delete=models.PROTECT)
    product_variant = models.ForeignKey(ProductVariants,on_delete=models.PROTECT)
    quantity = models.IntegerField()


    def __str__(self) -> str:
        return self.user.first_name


class UserOrders(BaseModel):

    user = models.ForeignKey(User,on_delete=models.PROTECT)
    payment_status = models.CharField(max_length=50,default="Paid")
    address = models.ForeignKey(UserAddress,on_delete=models.PROTECT,default=1)
    status = models.CharField(max_length=100,default='placed')


class UserOrderItems(BaseModel):

    user_order = models.ForeignKey(UserOrders,on_delete=models.PROTECT)
    product_variant = models.ForeignKey(ProductVariants,on_delete=models.PROTECT)
    quantity = models.IntegerField()
    status = models.CharField(max_length=100,default='placed')


class UserWishlist(BaseModel) :

    user = models.ForeignKey(User,on_delete=models.PROTECT)
    product_variant = models.ForeignKey(ProductVariants,on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.user.first_name