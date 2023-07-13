from django.db import models
from base.models import BaseModel
from users.models import User
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


class UserOrderItems(BaseModel):

    user_order = models.ForeignKey(UserOrders,on_delete=models.PROTECT)
    product_variant = models.ForeignKey(ProductVariants,on_delete=models.PROTECT)
    quantity = models.IntegerField()


class UserWishlist(BaseModel) :

    user = models.ForeignKey(User,on_delete=models.PROTECT)
    product_variant = models.ForeignKey(ProductVariants,on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.user.first_name