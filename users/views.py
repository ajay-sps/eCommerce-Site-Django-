from django.shortcuts import render,redirect
from rest_framework.views import APIView
from users.models import User,UserProfile
from django.http import HttpResponse
from users.serializer import UserSerializer
from base.email import verification_mail
from django.contrib.auth import authenticate,login,logout
from products.models import Products

class HomeView(APIView):

    def get(self,request):
        products = Products.objects.all()

        return render(request,'users/home.html',{'products':products})
    

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
                print(user.role.name)
                
                if user.role.name == 'admin':
                    login(request,user)
                    print('admin here')
                    return render(request,'users/home.html')
                elif user.role.name == 'buyer':
                    login(request,user)
                    print('buyer here')
                    return render(request,'users/home.html',{'buyer':'buyer'})
                else:
                    login(request,user)
                    print('seller here')
                    return render(request,'users/home.html',{'seller':'seller'})
                
            else:
                context = {"message" : "Email is not verified"}
                return render(request,'users/login.html',context)
                
        
        else :
            context = {"message" : "invalid email or password"}
            return render(request,'users/login.html',context)
    

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