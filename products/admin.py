from django.contrib import admin
from products.models import Brands,Categories,Products,ProductVariantProperties,ProductVariants,Properties,CategoryBanners


admin.site.register(Brands)
admin.site.register(Categories)
admin.site.register(ProductVariants)
admin.site.register(Products)
admin.site.register(ProductVariantProperties)
admin.site.register(Properties)
admin.site.register(CategoryBanners)

