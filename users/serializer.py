from rest_framework import serializers
from users.models import User,UserProfile,SellerInventory


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('address_line_1','state','city','contact','pincode')

class UserSerializer(serializers.ModelSerializer):

    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['username','first_name','last_name','password','email','profile','role']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        UserProfile.objects.create(user = user,**profile_data)

        return user
    

class SellerInvenotrySerializer(serializers.ModelSerializer):

    class Meta:
        model = SellerInventory
        fields = "__all__"