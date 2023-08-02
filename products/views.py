from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Brands,Categories,Products,Properties,ProductVariants,ProductVariantProperties
from django.http import HttpResponse
from products.serializer import ProductsSerializer,ProductVariantsSerializer,ProductVariantPropertiesSerializer,BrandsSerializer,CategoriesSerializer,PropertiesSerializer
import json
from django.core.paginator import Paginator
from django.db.models import Q
from orders.models import UserCart,UserWishlist
from users.permissions import AdminUser
# from eCommerce.document import BrandsDocument


class BrandsView(APIView):
    permission_classes = [AdminUser,]

    def get(self,request):
        try:
            print(type(request.GET.get('search')))
            search_item = False
            search_name =''
            if request.GET.get('search') != None:
                search_item = True
                search_name = request.GET.get('search')
                brands = Brands.objects.filter(name__icontains = request.GET.get('search')).order_by('-is_active','-id')
            else:
                brands = Brands.objects.order_by('-is_active','-id')
            item_per_page = 10
            paginator = Paginator(brands,item_per_page)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request,'products/brands.html',{'page_obj':page_obj,'search_item':search_item,'search_name':search_name})
        except Exception as e:
            return HttpResponse(str(e))
    

class AddBrandsView(APIView):
    permission_classes = [AdminUser,]
    
    def get(self,request):
        return render(request,'products/add_brands.html')
    
    def post(self,request):
        try:
            data = request.data 
            print(data)
            serializer = BrandsSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return redirect('/products/brands')
            else:
                return HttpResponse(serializer.errors)
        except Exception as e:
            return HttpResponse(str(e))
        

class UpdateBrandView(APIView):
    permission_classes = [AdminUser,]

    def get(self,request,id):
        brand = Brands.objects.get(id = id)
        return render(request,'products/update_brand.html',{'name': brand.name})
    
    def post(self,request,id):
        try:
            data = request.data
            brand_instance = Brands.objects.get(id = id)
            serializer = BrandsSerializer(brand_instance,data = data)
            if serializer.is_valid():
                serializer.save()
                return redirect(f'/products/brands')
            else:
                return HttpResponse(serializer.errors)
        except Exception as e:
            return HttpResponse(str(e))
    

class DeleteBrandView(APIView):
    permission_classes = [AdminUser,]
    
    def get(self,request,id):
        print('hello')
        brand_obj = Brands.objects.get(id = id)
        if brand_obj.is_active:
            brand_obj.is_active = False
        else:
            brand_obj.is_active = True
        brand_obj.save()
        print(11111111111)
        return Response('Ok')


class CategoriesView(APIView):
    permission_classes = [AdminUser,]

    def get(self,request):
        print(type(request.GET.get('search')))
        search_item = False
        search_name =''
        if request.GET.get('search') != None:
            search_item = True
            search_name = request.GET.get('search')
            categories = Categories.objects.filter(name__icontains = request.GET.get('search')).order_by('-is_active','-id')
        else:
            categories = Categories.objects.order_by('-is_active','-id')
        item_per_page = 10
        paginator = Paginator(categories,item_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number) 
        return render(request,'products/categories.html',{'page_obj':page_obj,'search_item':search_item,'search_name':search_name})
    

class AddCategoriesView(APIView):
    permission_classes = [AdminUser,]
    
    def get(self,request):
        return render(request,'products/add_categories.html')
    
    def post(self,request):
        try:
            data = request.data 
            serializer = CategoriesSerializer(data= data)
            if serializer.is_valid():
                serializer.save()
                return redirect('/products/categories')
            else:
                return HttpResponse(serializer.errors)
        except Exception as e:
            return HttpResponse(str(e))
        

class UpdateCategoryView(APIView):
    permission_classes = [AdminUser,]

    def get(self,request,id):
        category = Categories.objects.get(id = id)
        return render(request,'products/update_category.html',{'name': category.name})
    
    def post(self,request,id):
        try:
            data = request.data
            category_instance = Categories.objects.get(id = id)
            serializer = CategoriesSerializer(category_instance,data = data)
            if serializer.is_valid():
                serializer.save()
                return redirect(f'/products/categories')
            else:
                return HttpResponse(serializer.errors)
        except Exception as e:
            return HttpResponse(str(e))


class DeleteCategoryView(APIView):
    permission_classes = [AdminUser,]
    
    def get(self,request,id):
        category_obj = Categories.objects.get(id = id)
        if category_obj.is_active:
            category_obj.is_active = False
        else:
            category_obj.is_active = True
        category_obj.save()
        return Response('hi there')
    

class ProductsView(APIView):
    permission_classes = [AdminUser,]

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
                    products = Products.objects.filter(Q(name__icontains = search_list[0]) | Q(name__icontains = search_list[1])).order_by('-is_active','id')
                else:
                    products = Products.objects.filter(Q(name__icontains = request.GET['search']) | Q(name__icontains = request.GET['search'])).order_by('-id')
            else:
                products = Products.objects.order_by('-is_active','-id')
            item_per_page = 10
            paginator = Paginator(products,item_per_page)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request,'products/products.html',{"page_obj":page_obj, 'search_item':search_item,'search_name':search_name})
        except Exception as e:
            return HttpResponse(str(e))
    

class AddProductsView(APIView):
    permission_classes = [AdminUser,]

    def get(self,request):
        try:
            brands = Brands.objects.all()
            categories = Categories.objects.all()
            return render(request,'products/add_products.html',{'categories':categories,'brands':brands})
        except Exception as e:
            print(str(e))

    
    def post(self,request):
        try:
            data = request.data
            data['is_active'] = True if request.data.get('is_active') == 'on' else False
            serializer = ProductsSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                print(request.data.get('name'))
                product = Products.objects.get(name = request.data.get('name').strip())
                return redirect(f'/products/{product.id}/add/variants')
            else:
                return HttpResponse(serializer.errors)
        except Exception as e:
            print('exception error')
            return HttpResponse(str(e))


class AddProductVariantsView(APIView):
    permission_classes = [AdminUser,]

    def get(self,request,id):
        product = Products.objects.get(id = id)
        properties = Properties.objects.filter(is_active = True)
        list_properties = [property.name for property in properties ]
        context = {
            'name' : product.name,
            'id' : product.id,
            'brand_name' : product.brand.name,
            'category_name' : product.category.name,
            'properties' : json.dumps(list_properties),
        }
        return render(request,'products/add_product_variants.html',context)
    
    def post(self,request,id):
        try:
            data = request.data
            properties = data.getlist('property')
            values = data.getlist('value')
            product = Products.objects.get(id = id)
            data['product'] = id
            serializer = ProductVariantsSerializer(data = data)
            if serializer.is_valid():
                if ProductVariants.objects.filter(product = id).exists():
                    serializer.save()
                else:
                    serializer.save()
                    variant = ProductVariants.objects.get(code = data.get('code').strip())
                    variant.is_master = True
                    variant.save()

                print(data.get('code'))
                product_variant = ProductVariants.objects.get(code = data.get('code').strip())
                print(product_variant)
                print("=======================")
                for property,value in zip(properties,values):
                    property_object = Properties.objects.get(name = property)
                    property_data = {
                            'product_variant' : product_variant.id,
                            "property" : property_object.id,
                            'value' : value
                        }
                    property_serializer = ProductVariantPropertiesSerializer(data = property_data)
                    if property_serializer.is_valid():
                        property_serializer.save()
                    else :
                
                        return HttpResponse(property_serializer.errors)
                return redirect(f'/products/update/{product.id}')
            else:
                return HttpResponse(serializer.errors)
            
        except Exception as e:
            return HttpResponse(str(e))



class Test(APIView):

    def get(self,request):
        properties = Properties.objects.all()
        list_properties = [property.name for property in properties ]
        return render(request,'products/add_product_variants.html',{'properties':json.dumps(list_properties),"name":"ajay"})
    

class SpecificCategoryView(APIView):

    def get(self,request,name):
        try:
            product = Products.objects.filter(category__name = name.strip(),is_active = True,brand__is_active = True).order_by('?')
            products_variants = ProductVariants.objects.filter(product__in = product,is_master = True)
            products = []
            print(product,product.count())
            print(products_variants,products_variants.count())
            if request.GET.get('user_id') != "None":
                for item in product:
                    variant = ProductVariants.objects.filter(product = item,is_master = True)
                    if UserWishlist.objects.filter(product_variant = variant[0],user = request.GET.get('user_id')):
                        products.append({'product':item,'status':True})
                    else:
                        products.append({'product':item,'status':False})
            else:
                for item,variant in zip(product,products_variants):
                        products.append({'product':item,'status':False})

            return render(request,'products/category_details.html',{'products':products,'product_variant':products_variants,'category_name':name})
        except Exception as e:
            print(str(e))
            return HttpResponse(str(e))
    

class UpdateProductView(APIView):
    permission_classes = [AdminUser,]

    def get(self,request,id):
        brands = Brands.objects.all()
        categories = Categories.objects.all()
        product = Products.objects.get(id = id)
        product_variants = ProductVariants.objects.filter(product = id)
        variants_id = [variant.id for variant in product_variants]
        variant_properties = ProductVariantProperties.objects.filter(product_variant__id__in = variants_id )

        context = {
            "name" : product.name,
            "id" : product.id,
            "brand_name" : product.brand.name,
            "category_name" : product.category.name,
            "description" : product.description,
            "categories" : categories,
            "brands" : brands,
            'product_variants': product_variants,
            "variant_properties" : variant_properties,
        }

        if product.is_active:
            context["is_active"] = 'true'

        return render(request,'products/update_product.html',context)
    
    def post(self,request,id):
        try:
            data = request.data
            if "price" in data:
                product_id = id
                product = Products.objects.get(id = id)
                properties = data.getlist('property')
                values = data.getlist('value')
                property_ids = data.getlist('property_id')
                data['product'] =  id
                product_variant = ProductVariants.objects.get(id = data['variant_id'])
                variant_serializer = ProductVariantsSerializer(product_variant,data = data)
                if variant_serializer.is_valid():
                    variant_serializer.save()
                    for property,value,idd in zip(properties,values,property_ids):
                        property_object = Properties.objects.get(name = property)
                        property_data = {
                            'product_variant' : product_variant.id,
                            "property" : property_object.id,
                            'value' : value
                        }
                        variant_property_object = ProductVariantProperties.objects.get(id = idd)
                        property_serializer = ProductVariantPropertiesSerializer(variant_property_object,data = property_data)
                        if property_serializer.is_valid():
                            property_serializer.save()
                            print('saved')
                        else :
                            return HttpResponse(property_serializer.errors)
                return redirect(f'/products/update/{id}')
            
            else:
                product = Products.objects.get(id = id)
                serializer = ProductsSerializer(product,data = data)
                if serializer.is_valid():
                    serializer.save()
                    return redirect(f'/products')
                else:
                    return HttpResponse(serializer.errors)
                
        except Exception as e:
            return HttpResponse(str(e))


class DeleteProductView(APIView):
    permission_classes = [AdminUser,]
    
    def get(self,request,id):
        product_obj = Products.objects.get(id = id)
        if product_obj.is_active:
            product_obj.is_active = False
        else:
            product_obj.is_active = True
        product_obj.save()
        return Response('hi there')
    


class ProductDetailsView(APIView):

    def get(self,request,id):
        try:
            product = Products.objects.get(id = id)
            similar_products = Products.objects.filter(category = product.category,is_active = True,brand__is_active = True).order_by('?')[:6]
            print(similar_products.count(),similar_products)
            product_ids = [item.id for item in similar_products]
            user_id = request.GET.get('user_id')
            product_variants = ProductVariants.objects.filter(product = id)
            master_variant = ProductVariants.objects.get(product = id,is_master = True)
            similar_products_variants = ProductVariants.objects.filter(product__in = product_ids).exclude(id = master_variant.id).order_by('?')[:6]
            print(similar_products_variants.count())
            user_wishlist = False
            user_cart = False
            other_variants = False
            if user_id != "None":
                if UserCart.objects.filter(user = user_id,product_variant = master_variant):
                    user_cart = True
                if UserWishlist.objects.filter(user = user_id,product_variant = master_variant):
                    user_wishlist = True
            if len(product_variants) > 1 :
                other_variants = True
            variant_ids = [variant.id for variant in product_variants]
            product_variants_properties = ProductVariantProperties.objects.filter(product_variant__in = variant_ids)
            return render(request,'products/product_details.html',{'product_variants': product_variants,'product_variants_properties' : product_variants_properties,'id':id,'user_cart':user_cart,'user_wishlist':user_wishlist,'other_variants':other_variants,'similar_products':similar_products_variants,})
        except Exception as e:
            return HttpResponse(str(e))
    

class ProductVariantDetailsView(APIView):

    def get(self,request,id,variant_id):
        try:
            product = Products.objects.get(id = id)
            similar_products = Products.objects.filter(category = product.category,is_active = True,brand__is_active = True).order_by('?')[:6]
            product_ids = [item.id for item in similar_products]
            similar_products_variants = ProductVariants.objects.filter(product__in = product_ids).exclude(id = variant_id)[:6]
            user_id = request.GET.get('user_id')
            print(request.GET.get('user_id'))
            user_wishlist = False
            user_cart = False
            other_variants = False
            if user_id != "None":
                if UserCart.objects.filter(user = user_id,product_variant = variant_id):
                    user_cart = True
                if UserWishlist.objects.filter(user = user_id,product_variant = variant_id):
                    user_wishlist = True
            product_variants = ProductVariants.objects.filter(product = id)
            if len(product_variants) > 1:
                other_variants = True
            variant_ids = [variant.id for variant in product_variants]
            product_variants_properties = ProductVariantProperties.objects.filter(product_variant__in = variant_ids)
            return render(request,'products/product_variants_details.html',{'product_variants': product_variants,'product_variants_properties' : product_variants_properties,'id':id,"variant_id": variant_id,'user_cart':user_cart,'user_wishlist':user_wishlist,'other_variants':other_variants,'similar_products':similar_products_variants,})
        except Exception as e :
            return HttpResponse(str(e))
    

class ProductSearchView(APIView):

    def get(self,request):
        try:
            product = Products.objects.filter(name__icontains = request.GET.get('search'),is_active = True,category__is_active = True,brand__is_active = True)
            products_variants = ProductVariants.objects.filter(product__in = product,is_master = True)
            products = []
            if request.GET.get('user_id') != "None":
                for item in product:
                    products_variant_obj = ProductVariants.objects.get(product = item,is_master = True)
                    if UserWishlist.objects.filter(product_variant = products_variant_obj,user = request.GET.get('user_id')):
                        products.append({'product':item,'status':True})
                    else:
                        products.append({'product':item,'status':False})
            else:
                for item in product:
                    products.append({'product':item,'status':False})
            return render(request,'products/category_details.html',{'products':products,'product_variant':products_variants})
        except Exception as e:
            return HttpResponse(str(e))
    

class PropertiesView(APIView):
    permission_classes = [AdminUser,]

    def get(self,request):
        print(type(request.GET.get('search')))
        search_item = False
        search_name =''
        if request.GET.get('search') != None:
            search_item = True
            search_name = request.GET.get('search')
            properties = Properties.objects.filter(name__icontains = request.GET.get('search')).order_by('-is_active','-id')
        else:
            properties = Properties.objects.all().order_by('-is_active','-id')
        item_per_page = 10
        paginator = Paginator(properties,item_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,'products/properties.html',{'page_obj':page_obj,'search_item':search_item,'search_name':search_name})
    

class AddPropertiesView(APIView):
    permission_classes = [AdminUser,]

    def get(self,request):
        return render(request,'products/add_properties.html')
    
    def post(self,request):
        try:
            data = request.data 
            print(data)
            serializer = PropertiesSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return redirect('/products/properties')
            else:
                return HttpResponse(serializer.errors)
        except Exception as e:
            return HttpResponse(str(e))
        
        
class UpdatePropertiesView(APIView):
    permission_classes = [AdminUser,]

    def get(self,request,id):
        property = Properties.objects.get(id = id)
        return render(request,'products/update_property.html',{'name': property.name})
    
    def post(self,request,id):
        try:
            data = request.data
            property_instance = Properties.objects.get(id = id)
            serializer = PropertiesSerializer(property_instance,data = data)
            if serializer.is_valid():
                serializer.save()
                return redirect(f'/products/properties')
            else:
                return HttpResponse(serializer.errors)
        except Exception as e:
            return HttpResponse(str(e))


class DeletePropertiesView(APIView):
    permission_classes = [AdminUser,]
    
    def get(self,request,id):
        property_obj = Properties.objects.get(id = id)
        if property_obj.is_active:
            property_obj.is_active = False
        else:
            property_obj.is_active = True
        property_obj.save()
        return Response('hi there')
    

class DisplayAllProducts(APIView):

    def get(self,request):
        products = Products.objects.filter(is_active = True,category__is_active = True,brand__is_active = True).order_by('?')
        print(products.count())
        product_variants = ProductVariants.objects.filter(is_master = True,product__is_active = True)
        item_per_page = 30
        paginator = Paginator(products,item_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        print(type(paginator))
        
        return render(request,'products/all_products.html',{'page_obj':page_obj,'product_variants':product_variants,})
