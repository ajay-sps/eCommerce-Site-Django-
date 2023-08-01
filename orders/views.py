from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from orders.serializers import UserCartSerializer,UserWishlistSerializer,UserOrdersSerializer
from orders.models import UserCart,UserOrders,UserOrderItems,UserWishlist
from products.models import ProductVariantProperties,Products,ProductVariants
from django.http import HttpResponse
from django.conf import settings
import razorpay
from users.models import UserAddress,User
from users.tasks import order_mail,order_status_mail,send_sms
from django.core.paginator import Paginator
from django.db.models import Q


class UserCartView(APIView):
    def get(self,request,user_id):
        cart_items = UserCart.objects.filter(user__id = user_id)
        if cart_items:
            exist = True
        else:
            exist = False
        variant_ids = [item.product_variant.id for item in cart_items ]
        properties = ProductVariantProperties.objects.filter(product_variant__id__in = variant_ids)
        lst = []

        for item in cart_items:
            total_price = item.quantity * item.product_variant.price
            lst.append({'item': item,'total_price': total_price})
        return render(request,"orders/users_cart.html",{"items" : lst,'properties': properties,'exist': exist})


class AddItemsToUserCartView(APIView):

    def post(self,request,user_id):
        try:
            data = request.data
            serializer = UserCartSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors)
            return Response('hello')
        except Exception as e:
            return Response(str(e))
        

class UpdateCartItems(APIView):

    def put(self,request,user_id):
        print('hello')
        data = request.data
        obj = UserCart.objects.get(id = data['item_id'])
        obj.quantity = data['quantity']
        obj.save()
        return Response('Okk')

        
    
class DeleteUserCartItemView(APIView):

    def delete(self,request,user_id,item_id):
        obj = UserCart.objects.get(id = item_id)
        obj.delete()
        return Response('Ok')
    

class UserWishlistView(APIView):

    def get(self,request):
        user_id = request.GET.get('user_id')
        wishlist = UserWishlist.objects.filter(user = user_id)
        if wishlist:
            exist = True
        else:
            exist = False
        variant_ids = [item.product_variant.id for item in wishlist ]
        properties = ProductVariantProperties.objects.filter(product_variant__id__in = variant_ids)
        return render(request,'orders/users_wishlist.html',{'wishlist':wishlist,'properties': properties,'exist': exist,})
    

class AddItemsToUserWishlistView(APIView):

    def post(self,request,user_id):
        try:
            data = request.data
            serializer = UserWishlistSerializer(data = data)
            if serializer.is_valid():
                print("serializer is valid")
                serializer.save()
                return Response('OKk')
            else:
                print(serializer.errors)
                return Response(serializer.errors)
        except Exception as e:
            return Response(str(e))
        

class DeleteFromUserWishlistView(APIView):

    def post(self,request,user_id):
        try:
            data = request.data
            obj = UserWishlist.objects.get(user = data['user'] ,product_variant = data['product_variant'])
            obj.delete()
            return Response('Okk')
        except Exception as e:
            print(str(e))
            return HttpResponse(str(e))


class UserCartCheckOutView(APIView):

    def get(self,request,id):
        try:
            addresses = UserAddress.objects.filter(user = id)
            cart_items = UserCart.objects.filter(user = id )
            count  = cart_items.count()
            lst = []
            price = 0
            for item in cart_items:
                total_price = item.quantity * item.product_variant.price
                price += total_price
                lst.append({'item': item,'total_price': total_price})
            razor_price = price + 300
            client = razorpay.Client(auth = (settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
            data = { "amount": int(razor_price), "currency": "INR", "receipt": "order_rcptid_11" }
            payment = client.order.create(data = data)
            print(payment)
            return render(request,'orders/cart_checkout.html',{'cart':lst,'total_price':price,'payment':payment,'count':count,'addresses':addresses})
        except Exception as e:
            print(str(e))
            return Response(str(e))
        

class UserProductCheckoutView(APIView):

    def get(self,request,id):
        addresses = UserAddress.objects.filter(user = id)
        quantity = request.GET.get('quantity')
        product_variant = ProductVariants.objects.get(id = request.GET['variant_id'])
        price = product_variant.price * int(quantity)
        client = razorpay.Client(auth = (settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
        data = { "amount": int(price)+300, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data = data)
        print(price)
        return render(request,'orders/product_checkout.html',{'variant':product_variant,'price':price,'quantity':quantity,'payment':payment,'addresses':addresses})
    

class UserOrderPlacedView(APIView):

    def get(self,request,id):
        try:
            if 'quantity' in request.GET:
                user = User.objects.get(id = id)
                if request.GET.get('address_id'):
                    data = {"user": id,"payment_status" : "COD",'address':request.GET['address_id']}
                    address = UserAddress.objects.get(id = request.GET['address_id'])
                else:
                    data = {"user": id,"payment_status" : "Paid",'address':request.GET['address']}
                    address = UserAddress.objects.get(id = request.GET['address'])
                serializer = UserOrdersSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    print(serializer.instance.id)
                    user_order = UserOrders.objects.get(id = serializer.instance.id)
                    product_variant = ProductVariants.objects.get(id = request.GET['variant_id'])
                    UserOrderItems.objects.create(user_order = user_order,product_variant = product_variant,quantity = request.GET['quantity'])
                    mail = user.username
                    print("--------------------------------------------------",mail)
                    name = user.first_name
                    item_count = 1
                    total = int(product_variant.price) * int(request.GET['quantity'])
                    house = address.house_no
                    street = address.street
                    city = address.city
                    state = address.state
                    pincode = address.postal_code
                    order_mail.delay(mail,name,item_count,total,house,street,city,state,pincode)
                    return Response("i am here")
                else:
                    print(serializer.errors)
                    return Response(serializer.errors)
                
            else:
                user = User.objects.get(id = id)
                cart_items = UserCart.objects.filter(user = id)
                item_count = cart_items.count()
                total = 0
                print(request.GET.get('address_id'))
                if request.GET.get('address_id'):
                    data = {"user": id,"payment_status" : "COD",'address':request.GET['address_id']}
                    address = UserAddress.objects.get(id = request.GET['address_id'])
                else:
                    data = {"user": id,"payment_status" : "Paid",'address':request.GET['address']}
                    address = UserAddress.objects.get(id = request.GET['address'])
                serializer = UserOrdersSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    print(serializer.instance.id)
                    user_order = UserOrders.objects.get(id = serializer.instance.id)
                    for item in cart_items:
                        UserOrderItems.objects.create(user_order = user_order,product_variant = item.product_variant,quantity = item.quantity)
                        total += int(item.product_variant.price) * int(item.quantity)
                        item.delete()
                    mail = user.username
                    print("--------------------------------------------------",mail)
                    name = user.first_name
                    house = address.house_no
                    street = address.street
                    city = address.city
                    state = address.state
                    pincode = address.postal_code 
                    order_mail.delay(mail,name,item_count,total,house,street,city,state,pincode)
                    return Response("i am here")
                else:
                    print(serializer.errors)
                    return Response(serializer.errors)
        except Exception as e:
            print(str(e))
            return Response(str(e))


class UserOrdersView(APIView):

    def get(self,request,id):
        try:
            wishlist_count = UserWishlist.objects.filter(user = id).count()
            cart_count = UserCart.objects.filter(user = id).count()
            orders = UserOrders.objects.filter(user = id).order_by('-id')
            order_count = orders.count()
            return render(request,'orders/user_orders.html',{'orders':orders,'wishlist_count':wishlist_count,'cart_count':cart_count,'order_count':order_count})
        except Exception as e:
            return HttpResponse(str(e))
    

class UserOrdersDetailView(APIView):

    def get(self,request,id):
        print(request.GET['order_id'])
        order = UserOrders.objects.get(id = request.GET['order_id'])
        order_items = UserOrderItems.objects.filter(user_order = request.GET['order_id'])
        total_price = 0
        for item in order_items:
            total_price += int(item.quantity)*int(item.product_variant.price)
        print(order_items,total_price)
        return render(request,'orders/user_order_details.html',{'order_items':order_items,'order':order,'total_price':total_price,'items_count':order_items.count()})
    

class OrdersView(APIView):

    def get(self,request):
        try:
            search_item = False
            search_name =''
            if request.GET.get('search'):
                search_item = True 
                search_name += request.GET.get('search')
                search_list = request.GET.get('search').split(' ')
                print(search_list)
                if len(search_list)>1:
                    orders = UserOrders.objects.filter(Q(user__first_name__icontains = search_list[0]) | Q(user__last_name__icontains = search_list[1]))
                else:
                    orders = UserOrders.objects.filter(Q(user__first_name__icontains = request.GET['search']) | Q(user__last_name__icontains = request.GET['search'])).order_by('-id')
            else:
                orders = UserOrders.objects.all().order_by('-id')
            lst = []
            for order in orders:
                price = 0
                items = UserOrderItems.objects.filter(user_order = order)
                for item in items:
                    price += int(item.product_variant.price) * int(item.quantity)
                lst.append({'order':order,'price': price})
            item_per_page = 10
            paginator = Paginator(lst,item_per_page)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request,'orders/orders.html',{"page_obj":page_obj,'search_item':search_item,'search_name':search_name})
        except Exception as e:
            return HttpResponse(str(e)) 
            
    

class OrderDetailView(APIView):

    def get(self,request):
        data = request.GET
        order_items = UserOrderItems.objects.filter(user_order = data['order_id'])
        item_per_page = 10
        paginator = Paginator(order_items,item_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        print(order_items)
        return render(request,'orders/order_details.html',{"page_obj":page_obj})
    

class UpdateOrderStatusView(APIView):

    def get(self,request):
        data = request.GET
        order = UserOrders.objects.get(id = data['order_id'])
        return render(request,'orders/update_order_status.html',{'order':order})
    
    def post(self,request):
        try:
            data = request.data
            print(data)
            order = UserOrders.objects.get(id = data['order_id'])
            items = []
            order_items = UserOrderItems.objects.filter(user_order = order)
            for item in order_items:
                items.append(item.product_variant.product.name)
            print(items)
            user = order.user.first_name
            email = order.user.username
            status = data['status']
            order_status_mail.delay(email,status,items,user)
            print(type(order.user.profile.contact))
            phone = "+91" + order.user.profile.contact
            message = f"you order has been {status}"
            print(message)
            send_sms.delay(phone,message)
            order.status = status
            order.save()
            return redirect('/cart/orders')
        except Exception as e:
            return HttpResponse(str(e))