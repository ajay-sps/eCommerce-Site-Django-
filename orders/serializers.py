from rest_framework import serializers
from orders.models import UserCart,UserOrderItems,UserOrders,UserWishlist


class UserCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCart
        fields = "__all__"


class UserWishlistSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserWishlist
        fields = "__all__"


class UserOrdersSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserOrders
        fields = "__all__"