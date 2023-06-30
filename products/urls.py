from django.urls import path
from products.views import BrandsView,CategoriesView,ProductsView,AddProductsView,Test,SpecificCategoryView,UpdateProductView,AddProductVariantsView,AddBrandsView,AddCategoriesView,UpdateCategoryView,UpdateBrandView,ProductDetailsView,ProductVariantDetailsView


urlpatterns = [
    path('',ProductsView.as_view()),
    path('<int:id>/details',ProductDetailsView.as_view()),
    path('<int:id>/details/<int:variant_id>',ProductVariantDetailsView.as_view()),
    path('add/',AddProductsView.as_view()),
    path('update/<int:id>',UpdateProductView.as_view()),
    path('<int:id>/add/variants',AddProductVariantsView.as_view()),
    path('brands/',BrandsView.as_view()),
    path('brands/add',AddBrandsView.as_view()),
    path('brands/update/<int:id>',UpdateBrandView.as_view()),
    path('categories/',CategoriesView.as_view()),
    path('categories/add',AddCategoriesView.as_view()),
    path('categories/update/<int:id>',UpdateCategoryView.as_view()),
    path('categories/<str:name>',SpecificCategoryView.as_view()),
    path('test/',Test.as_view()),
]