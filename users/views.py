from django.shortcuts import render,redirect
from rest_framework.views import APIView
from users.models import User,UserProfile,SellerInventory,UserAddress
from django.http import HttpResponse
from users.serializer import UserSerializer,SellerInvenotrySerializer,UserAddressesSerialiazer,UpdateUserSerializer
from django.contrib.auth import authenticate,login,logout
from products.models import Products,ProductVariants,Categories,ProductVariantProperties,Properties,Brands,CategoryBanners
from django.core.paginator import Paginator
from rest_framework.response import Response
# from users.tasks import verification_mail,password_reset_mail
from orders.models import UserWishlist,UserCart,UserOrders
from django.core.mail import send_mail,EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from twilio.rest import Client

# function defined to send emails

def verification_mail(token,email,name):
    try:
        context = {
            'token' : token,
            'name' : name ,
        }
        subject = 'Email Verification'
        template = 'users/email_verification_email_template.html'
        html_content = render_to_string(template,context)

        email = EmailMessage(subject,html_content,to=[email])
        email.content_subtype = 'html'
        email.send()
        
        return f'mail sent successfully'
    except Exception as e:
        print(str(e))

class HomeView(APIView):

    def get(self,request):
        try:
            first_banner = CategoryBanners.objects.filter(category__is_active = True).order_by('?')[:1]
            banner_id = []
            for item in first_banner:
                banner_id.append(item.id)
            other_banners = CategoryBanners.objects.filter(category__is_active = True).exclude(id__in = banner_id).order_by('?')[:3]
            products = Products.objects.filter(is_active = True,category__is_active=True,brand__is_active = True).order_by('?')[:12]
            product_variants = ProductVariants.objects.filter(is_master = True,product__is_active = True)
            categories = Categories.objects.filter(is_active = True).order_by('?')
            return render(request,'users/home.html',{'products':products ,'categories' : categories,'product_variants':product_variants,'first_banner':first_banner,'other_banners':other_banners})
        except Exception as e:
            print(str(e))
            return HttpResponse(str(e))
    


class LoginView(APIView):

    def get(self,request):
        try:
            verified = False
            try:
                if request.GET.get('verified'):
                    verified = True
            except:
                pass
            return render(request,'users/login.html',{'verified':verified})
        except Exception as e:
            return HttpResponse(str(e))
    
    def post(self,request):
        data = request.data
        username = data.get('email')
        password = data.get('password')
        print(username,password)

        user = authenticate(username = username,password = password)
        if user is not None:
            if user.is_verified == True:
                if user.role.name == 'admin':
                    login(request,user)
                    return redirect('/dashboard')
                else:
                    login(request,user)
                    return redirect('/')
            else:
                return render(request,'users/login.html',{"message" : "Email is not verified !"})
        else :
            user_obj = User.objects.filter(username = username)
            print(user,user_obj)
            return render(request,'users/login.html',{"message" : "Invalid email or password !"})
    

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
                verification_mail(token,arranged_data.get('email'),user.first_name)
                context = {'success':'An Email has been sent for Email Verification'}
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

            return redirect('/login?verified=True')
        
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
            addresses = UserAddress.objects.filter(user = request.GET['user_id']).order_by('-id')
            return render(request,'users/profile.html',{'addresses':addresses})
        except Exception as e:
            return Response(str(e))
    

class AdminDashboardView(APIView):

    def get(self,request):
        products = Products.objects.count()
        categories = Categories.objects.count()
        brands = Brands.objects.count()
        orders = UserOrders.objects.count()
        properties = Properties.objects.count()
        print(products,categories,brands,orders)
        return render(request,'users/dashboard.html',{"products":products,"categories":categories,'brands':brands,"orders":orders,'properties':properties})
    

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
                print('hello')
                serialiazer.save()
                return redirect(f'/users/profile?user_id={data["user"]}')
            else:
                print('byuee')
                return Response(serialiazer.errors)
        except Exception as e:
            print(str(e))
            return Response(str(e))
        

class UpdateUserAddressView(APIView):

    def get(self,request):
        try:
            address = UserAddress.objects.get(id = request.GET['address_id']) 
            return render(request,'users/update_address.html',{'address':address})
        except Exception as e:
            return Response(str(e))
        
    def post(self,request):
        try:
            data = request.data
            address_instance = UserAddress.objects.get(id = data['address_id'])
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
            address = UserAddress.objects.get(id = address_id)
            address.delete()
            return Response('Deleted Successfully')
        except Exception as e:
            return Response(str(e))
        

class ForgotPasswordView(APIView):

    def get(self,request):
        return render(request,'users/forgot_password.html')
    
    def post(self,request):
        data = request.data
        if User.objects.filter(username = data['email']):
            user = User.objects.get(username = data['email'])
            user.profile.generate_token()
            token = user.profile.token
            name = user.first_name
            password_reset_mail.delay(data['email'],token,name)
            message = "check your mail to proceed further"
        else:
            message = 'This mail is not registered !'
        return render(request,'users/forgot_password.html',{'message':message})
    

class ResetPasswordView(APIView):

    def get(self,request,token):
        if UserProfile.objects.filter(token = token):
            return render(request,'users/reset_password.html')
        else:
            return render(request,'users/reset_password.html',{'expired':'token expired'})
    
    def post(self,request,token):
        try:
            data = request.data
            if data['password1'] == data['password2']:
                if len(data['password1']) < 5 :
                    message = 'Please enter password of length 5 or greater '
                else :
                    user = User.objects.get(profile__token = token)
                    user.set_password(data['password1'])
                    print(user,data['password1'])
                    user.save()
                    profile = UserProfile.objects.get(token = token)
                    profile.token = None
                    profile.save()
                    message = 'Password Changed Successfully'
            else : 
                message = "confirm password and password did not match"
            print(data,token)
            return render(request,'users/reset_password.html',{'message':message})
        except Exception as e :
            return HttpResponse(str(e))
        

class GetUserCartWishlishCount(APIView):

    def get(self,request):
        if request.user.id != None:
            wishlist_count = UserWishlist.objects.filter(user = request.user).count()
            cart_count = UserCart.objects.filter(user = request.user).count()
            print(wishlist_count,cart_count)
            return Response({'wishlist_count':wishlist_count,'cart_count':cart_count})
        else:
            return Response('Ok')

        
class AdminProfileView(APIView):

    def get(self,request):
        return render(request,'users/admin_profile.html')
    

class AdminProfileUpdateView(APIView):
    
    def get(self,request):
        return render(request,'users/admin_profile_update.html')
    
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
                return redirect(f"/admin_profile")
            else:
                return Response(serializer.errors)
        except Exception as e:
            return Response(str(e))
        
    
class AboutUsView(APIView):

    def get(self,request):
        return render(request,'users/about_us.html')