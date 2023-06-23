from django.urls import path
from products.views import BrandsView,CategoriesView,ProductsView,AddProductsView


urlpatterns = [
    path('',ProductsView.as_view()),
    path('add/',AddProductsView.as_view()),
    path('brands/',BrandsView.as_view()),
    path('categories/',CategoriesView.as_view()),
]