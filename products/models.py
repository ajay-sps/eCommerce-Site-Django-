from django.db import models
from base.models import BaseModel



class Brands(BaseModel):

    name = models.CharField(max_length=40,unique=True)
    image = models.ImageField(upload_to='products/brands')
    is_active = models.BooleanField(default= True)

    def __str__(self) -> str:
        return self.name


class Categories(BaseModel):

    name = models.CharField(max_length=40,unique=True)
    image = models.ImageField(upload_to='products/categories')
    is_active = models.BooleanField(default= True)

    def __str__(self) -> str:
        return self.name
    

class Products(BaseModel):

    brand = models.ForeignKey(Brands,on_delete=models.PROTECT,related_name='product')
    category = models.ForeignKey(Categories,on_delete=models.PROTECT,related_name='product')
    name = models.CharField(max_length=50,unique=True)
    image = models.ImageField(upload_to='products/products',default= None)
    description = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class Properties(BaseModel):
    
    name = models.CharField(max_length=20,unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class ProductVariants(BaseModel):
    
    product = models.ForeignKey(Products,on_delete=models.PROTECT,related_name='product_variant')
    image = models.ImageField(upload_to='products/product_variants')
    code = models.CharField(max_length=30,unique=True,default='123')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    is_master = models.BooleanField(default=False)
    is_active = models.BooleanField(default= True)

    def __str__(self) -> str:
        return self.code


class ProductVariantProperties(BaseModel):

    product_variant = models.ForeignKey(ProductVariants,on_delete=models.PROTECT,related_name='product_variant_properties')
    property = models.ForeignKey(Properties,on_delete=models.PROTECT,related_name='product_variant_properties')
    value = models.CharField(max_length=30,default='red')

    def __str__(self) -> str:
        return self.product_variant.code
    

class CategoryBanners(BaseModel):

    category = models.OneToOneField(Categories,on_delete=models.PROTECT)
    image = models.ImageField(upload_to='products/category_banner')

    def __str__(self) -> str:
        return self.category.name