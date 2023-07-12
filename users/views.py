from django.shortcuts import render,redirect
from rest_framework.views import APIView
from users.models import User,UserProfile,SellerInventory,UserAddresses
from django.http import HttpResponse
from users.serializer import UserSerializer,SellerInvenotrySerializer,UserAddressesSerialiazer,UpdateUserSerializer
from base.email import verification_mail
from django.contrib.auth import authenticate,login,logout
from products.models import Products,ProductVariants,Categories,ProductVariantProperties,Properties,Brands
from django.core.paginator import Paginator
from rest_framework.response import Response


class HomeView(APIView):

    def get(self,request):
        first_product = Products.objects.first()
        products = Products.objects.all()[1:9]
        product_variants = ProductVariants.objects.filter(is_master = True)
        categories = Categories.objects.all()
        return render(request,'users/home.html',{'products':products ,'categories' : categories,'first_product':first_product,'product_variants':product_variants})
    

class LoginView(APIView):

    def get(self,request):
        return render(request,'users/login.html')
    
    def post(self,request):
        data = request.data
        username = data.get('email')
        password = data.get('password')

        user = authenticate(username = username,password = password)
        if user is not None:
            if user.is_verified == True:
                login(request,user)
                return redirect('/')
            else:
                return render(request,'users/login.html',{"message" : "Email is not verified"})
        else :
            return render(request,'users/login.html',{"message" : "invalid email or password"})
    

class SignupView(APIView):

    def get(self,request):
        return render(request,'users/signup.html')
    
    def post(self,request):
        try : 
            data = request.data
            arranged_data = {
                'username' : data.get('email'),
                'email' : data.get('email'),
                'password' : data.get('password'),
                'first_name' : data.get('first_name'),
                'last_name' : data.get('last_name'),
                'role' : data.get('role',1),
                'profile' : {
                    'state' : data.get('state'),
                    'city' : data.get('city'),
                    'contact' : data.get('contact'),
                    'pincode' : data.get('pincode'),
                    'address_line_1' : data.get('address_line_1')
                }
            }
            serializer = UserSerializer(data = arranged_data)

            if serializer.is_valid():
                user = serializer.save()
                user.profile.generate_token()
                token = user.profile.token
                verification_mail(token,arranged_data.get('email'))
                context = {'success':'User Created Successfully'}
                return render(request,'users/signup.html',context)
            else:
                for key,value in serializer.errors.items():
                    print(key,value)
                arranged_data['errors'] = serializer.errors
                return render(request,'users/signup.html',arranged_data)
            
        except Exception as e:
            print(str(e))
            return HttpResponse('hi')


class TokenVerificationView(APIView):

    def get(self,request,token):
        try:
            profile = UserProfile.objects.get(token = token)
            user = profile.user
            user.is_verified = True
            user.save()
            profile.token = None
            profile.save()

            return redirect('/login')
        
        except Exception as e:
            return HttpResponse(str(e))



class LogOutView(APIView):

    def get(self,request):
        logout(request)
        return redirect('/')
    

class SellersView(APIView):

    def get(self,request):
        sellers = User.objects.filter(role__name = "seller")
        item_per_page = 5
        paginator = Paginator(sellers,item_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,'sellers/sellers.html',{"page_obj":page_obj})
    

class SellersInvetoryView(APIView):

    def get(self,request,id):
        seller_inventory = SellerInventory.objects.filter(seller = id)
        item_per_page = 5
        i = 1
        lst = []
        for seller in seller_inventory :
            lst.append({'seller': seller,'serial_no' : i})
            i += 1
        paginator = Paginator(lst,item_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,'sellers/sellers_inventory.html',{'page_obj': page_obj,'id':id})


class UpdateInventoryItemsView(APIView):

    def get(self,request,id,inventory_id):
        inventory = SellerInventory.objects.get(id = inventory_id)
        return render(request,'sellers/sellers_update_inventory.html',{'inventory_obj' : inventory,"id": id, "inventory_id" : inventory_id})
    
    def post(self,request,id,inventory_id):
        try:
            data = request.data
            inventory_instance = SellerInventory.objects.get(id = inventory_id)
            serializer = SellerInvenotrySerializer(inventory_instance,data = data)
            if serializer.is_valid():
                serializer.save()
                return redirect(f'/sellers/{id}/inventory')
            else:
                return HttpResponse(serializer.errors)
        except Exception as e:
            return HttpResponse(str(e))
        

class SellerProductsView(APIView):

    def get(self,request,id):
        products = Products.objects.all()
        item_per_page = 5
        i = 1
        lst = []
        for product in products:
            lst.append({"product" : product,"serial_no" : i})
            i += 1
        paginator = Paginator(lst,item_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,'sellers/sellers_products.html',{"page_obj":page_obj,'id':id})
    

class SellerAddVariantsView(APIView):

    def get(self,request,id,product_id):
        product = Products.objects.get(id = product_id)
        product_variants = ProductVariants.objects.filter(product = product.id)
        variants_id = [variant.id for variant in product_variants]
        variant_properties = ProductVariantProperties.objects.filter(product_variant__id__in = variants_id )

        context = {
            "seller_id" : id,
            "name" : product.name,
            "id" : product.id,
            "brand_name" : product.brand.name,
            "category_name" : product.category.name,
            "description" : product.description,
            'product_variants': product_variants,
            "variant_properties" : variant_properties,
        }

        if product.is_active:
            context["is_active"] = 'true'

        return render(request,'sellers/sellers_add_product.html',context)
    
    def post(self,request,id,product_id):
        try:
            data = request.data
            if SellerInventory.objects.filter(product_variant = data['product_variant']):
                obj = SellerInventory.objects.get(product_variant = data['product_variant'])
                obj.quantity += int(data['quantity'])
                obj.save()
                print(id)
                return redirect(f'/sellers/{id}/inventory')
            else:
                for item in data:
                    print(item)
                serializer = SellerInvenotrySerializer(data = data)
                if serializer.is_valid():
                    serializer.save()
                    return redirect(f'/sellers/{id}/inventory')
                else:
                    return HttpResponse(serializer.errors)
        except Exception as e:
            return HttpResponse(str(e))
        

class UserProfileView(APIView):

    def get(self,request):
        try:
            addresses = UserAddresses.objects.filter(user = request.GET['user_id'])
            return render(request,'users/profile.html',{'addresses':addresses})
        except Exception as e:
            return Response(str(e))
    

class AdminDashboardView(APIView):

    def get(self,request):
        products = Products.objects.count()
        categories = Categories.objects.count()
        brands = Brands.objects.count()
        sellers = User.objects.filter(role__name = 'seller').count()
        print(products,categories,brands,sellers)
        return render(request,'users/dashboard.html',{"products":products,"categories":categories,'brands':brands,"sellers":sellers})
    

class UpdateUserProfileView(APIView):

    def get(self,request):
        return render(request,'users/update_profile.html')
    
    def post(self,request):
        try:
            data = request.data
            print(data)
            arranged_data = {
                    'first_name' : data.get('first_name'),
                    'last_name' : data.get('last_name'),
                    'profile' : {
                        'state' : data.get('state'),
                        'city' : data.get('city'),
                        'contact' : data.get('contact'),
                        'profile_image' : data.get('image'),
                    }
                }
            user_instance = User.objects.get(id = data['user_id'])
            serializer = UpdateUserSerializer(user_instance,data = arranged_data)
            if serializer.is_valid():
                serializer.save()
                return redirect(f"/users/profile?user_id={data['user_id']}")
            else:
                return Response(serializer.errors)
        except Exception as e:
            return Response(str(e))
        
    

class AddUserAddressView(APIView):

    def get(self,request):
        return render(request,'users/add_address.html')
    
    def post(self,request):
        try:
            data = request.data
            serialiazer = UserAddressesSerialiazer(data = data)
            if serialiazer.is_valid():
                serialiazer.save()
                return redirect(f'/users/profile?user_id={data["user"]}')
            else:
                return Response(serialiazer.errors)
        except Exception as e:
            return Response(str(e))
        

class UpdateUserAddressView(APIView):

    def get(self,request):
        try:
            address = UserAddresses.objects.get(id = request.GET['address_id']) 
            return render(request,'users/update_address.html',{'address':address})
        except Exception as e:
            return Response(str(e))
        
    def post(self,request):
        try:
            data = request.data
            address_instance = UserAddresses.objects.get(id = data['address_id'])
            serializer = UserAddressesSerialiazer(address_instance,data=data)
            if serializer.is_valid():
                serializer.save()
                return redirect(f'/users/profile?user_id={data["user"]}')
            else :
                return Response(serializer.errors)
        except Exception as e :
            return Response(str(e))


class DeleteUserAddressView(APIView):

    def delete(self,request,address_id):
        try:
            address = UserAddresses.objects.get(id = address_id)
            address.delete()
            return Response('Deleted Successfully')
        except Exception as e:
            return Response(str(e))