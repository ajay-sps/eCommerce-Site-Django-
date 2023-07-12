from rest_framework import serializers
from users.models import User,UserProfile,SellerInventory,UserAddresses


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('address_line_1','state','city','contact','pincode')


class UpdateUserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('state','city','contact','profile_image')


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
    

class UpdateUserSerializer(serializers.ModelSerializer):

    profile = UpdateUserProfileSerializer()

    class Meta:
        model = User
        fields = ['first_name','last_name','profile']
    

class SellerInvenotrySerializer(serializers.ModelSerializer):

    class Meta:
        model = SellerInventory
        fields = "__all__"


class UserAddressesSerialiazer(serializers.ModelSerializer):

    class Meta:
        model = UserAddresses
        fields = "__all__"