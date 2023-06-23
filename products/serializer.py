from rest_framework import serializers
from products.models import Products,ProductVariants,ProductVariantProperties


class ProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = '__all__'


class ProductVariantsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariants
        fields = '__all__'


class ProductVariantPropertiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariantProperties
        fields = '__all__'