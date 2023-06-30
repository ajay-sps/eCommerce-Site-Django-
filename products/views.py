from django.shortcuts import render,redirect
from rest_framework.views import APIView
from products.models import Brands,Categories,Products,Properties,ProductVariants,ProductVariantProperties
from django.http import HttpResponse
from products.serializer import ProductsSerializer,ProductVariantsSerializer,ProductVariantPropertiesSerializer,BrandsSerializer,CategoriesSerializer
import json
from django.core.paginator import Paginator


class BrandsView(APIView):

    def get(self,request):
        brands = Brands.objects.all()
        i = 1
        lst = []
        for brand in brands:
            lst.append({"brand" : brand,"serial_no" : i})
            i += 1
        item_per_page = 5
        paginator = Paginator(lst,item_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        print(len(page_obj))
        return render(request,'products/brands.html',{'page_obj':page_obj})
    

class AddBrandsView(APIView):
    
    def get(self,request):
        return render(request,'products/add_brands.html')
    
    def post(self,request):
        try:
            data = request.data 
            serializer = BrandsSerializer(data= data)
            if serializer.is_valid():
                serializer.save()
                return redirect('/products/brands')
            else:
                return HttpResponse(serializer.errors)
        except Exception as e:
            return HttpResponse(str(e))
        

class UpdateBrandView(APIView):

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
    

class CategoriesView(APIView):

    def get(self,request):
        categories = Categories.objects.all()
        item_per_page = 5
        i = 1
        lst = []
        for category in categories:
            lst.append({"category" : category,"serial_no" : i})
            i += 1
        paginator = Paginator(lst,item_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number) 
        return render(request,'products/categories.html',{'page_obj':page_obj})
    

class AddCategoriesView(APIView):
    
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

    

class ProductsView(APIView):

    def get(self,request):
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
        return render(request,'products/products.html',{"page_obj":page_obj})
    

class AddProductsView(APIView):

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
                product = Products.objects.get(name = request.data.get('name'))
                return redirect(f'/products/{product.id}/add/variants')
            else:
                return HttpResponse(serializer.errors)
        except Exception as e:
            print('exception error')
            return HttpResponse(str(e))


class AddProductVariantsView(APIView):

    def get(self,request,id):
        product = Products.objects.get(id = id)
        properties = Properties.objects.all()
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
                    variant = ProductVariants.objects.get(code = data.get('code'))
                    variant.is_master = True
                    variant.save()
                product_variant = ProductVariants.objects.get(code = data.get('code'))
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
        products = Products.objects.filter(category__name = name)
        print('hello')
        print(products)
        return render(request,'products/category_details.html',{'products':products})
    

class UpdateProductView(APIView):

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
                    return redirect(f'/products/update/{id}')
                else:
                    return HttpResponse(serializer.errors)
                
        except Exception as e:
            return HttpResponse(str(e))
        

class ProductDetailsView(APIView):

    def get(self,request,id):
        product_variants = ProductVariants.objects.filter(product = id)
        variant_ids = [variant.id for variant in product_variants]
        product_variants_properties = ProductVariantProperties.objects.filter(product_variant__in = variant_ids)
        return render(request,'products/product_details.html',{'product_variants': product_variants,'product_variants_properties' : product_variants_properties,'id':id})
    

class ProductVariantDetailsView(APIView):

    def get(self,request,id,variant_id):
        product_variants = ProductVariants.objects.filter(product = id)
        variant_ids = [variant.id for variant in product_variants]
        product_variants_properties = ProductVariantProperties.objects.filter(product_variant__in = variant_ids)
        return render(request,'products/product_variants_details.html',{'product_variants': product_variants,'product_variants_properties' : product_variants_properties,'id':id,"variant_id": variant_id})