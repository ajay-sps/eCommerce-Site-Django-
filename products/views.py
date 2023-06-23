from django.shortcuts import render,redirect
from rest_framework.views import APIView
from products.models import Brands,Categories,Products,Properties,ProductVariants,ProductVariantProperties
from django.http import HttpResponse
from products.serializer import ProductsSerializer,ProductVariantsSerializer,ProductVariantPropertiesSerializer


class BrandsView(APIView):

    def get(self,request):
        brands = Brands.objects.all()
        return render(request,'products/brands.html',{'brands':brands})
    

class CategoriesView(APIView):

    def get(self,request):
        categories = Categories.objects.all()
        return render(request,'products/categories.html',{'categories':categories})
    

class ProductsView(APIView):

    def get(self,request):
        return render(request,'products/products.html')
    


class AddProductsView(APIView):

    def get(self,request):
        try:
            brands = Brands.objects.all()
            categories = Categories.objects.all()
            products = Products.objects.all()
            return render(request,'products/add_products.html',{'categories':categories,'brands':brands,'products':products})
        except Exception as e:
            print(str(e))
    
    def post(self,request):
        try:
            data = request.data
            if 'price' in data :
                data = request.data
                print(request.data.get('product'))
                product = Products.objects.get(name = request.data.get('product'))
                data['product'] = product.id
                serializer = ProductVariantsSerializer(data = data)
                if serializer.is_valid():
                    serializer.save()
                    print('after validation')
                    properties = Properties.objects.all()
                    context = {
                        'name' : product.name,
                        'brand' : product.brand.name,
                        'category' : product.category.name,
                        'product_image' : product.image,
                        'description' : product.description,
                        'is_active' : product.is_active,
                        'code' : data['code'],
                        'price' : data['price'],
                        'product_variant_image' : data['image'],
                        'properties' : properties,
                    }
                    print('--------------------------------')
                    return render(request,'products/add_product_variant_properties.html',context)
                else:
                    print('error')
                    return HttpResponse(serializer.errors)
                
            elif 'property' in data:
                
                data = request.data
                product_variant = ProductVariants.objects.get(code = request.data.get('product_variant'))
                product = product_variant.product
                print('hello')
                print(type(data))
                print(product_variant.id)
                data_set = {
                    'product_variant' : product_variant.id,
                    'property' : data.get('property'),
                    'value' : data.get('value'),
                }
                # data['product_variant'] = product_variant.id
                print('------------')
                serializer = ProductVariantPropertiesSerializer(data= data_set)
                if serializer.is_valid():
                    serializer.save()
                    properties = Properties.objects.all()
                    context = {
                        'name' : product.name,
                        'brand' : product.brand.name,
                        'category' : product.category.name,
                        'product_image' : product.image,
                        'description' : product.description,
                        'is_active' : product.is_active,
                        'code' : product_variant.code,
                        'price' : product_variant.price,
                        'product_variant_image' : product_variant.image,
                        'properties' : properties,
                    }
                    return render(request,'products/add_product_variant_properties_again.html',context)
            
            else:
                data = request.data
                data['is_active'] = True if request.data.get('is_active') == 'on' else False
                serializer = ProductsSerializer(data = data)
                if serializer.is_valid():
                    serializer.save()
                    product = Products.objects.get(name = request.data.get('name'))
                    context = {
                        'name' : product.name,
                        'brand' : product.brand.name,
                        'category' : product.category.name,
                        'image' : product.image,
                        'description' : product.description,
                        'is_active' : product.is_active,
                    }
                    return render(request,'products/add_product_variants.html',context)
                else:
                    return HttpResponse(serializer.errors)
        except Exception as e:
            print('exception error')
            return HttpResponse(str(e))

