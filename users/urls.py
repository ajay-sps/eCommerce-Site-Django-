from django.urls import path
from users.views import HomeView,LoginView,SignupView,TokenVerificationView,LogOutView,SellersView,SellersInvetoryView,UpdateInventoryItemsView,SellerProductsView,SellerAddVariantsView,UserProfileView,AdminDashboardView,UserProfileUpdateView,AddUserAddressView,UpdateUserAddressView,DeleteUserAddressView



urlpatterns = [
    path('',HomeView.as_view(),name='homepage'),
    path('login/',LoginView.as_view(),name='login_page'),
    path('signup/',SignupView.as_view(),name='signup_page'),
    path('logout/',LogOutView.as_view(),name='logout_page'),
    path('sellers/',SellersView.as_view(),name='logout_page'),
    path('sellers/<int:id>/inventory/',SellersInvetoryView.as_view(),name='seller_inventory'),
    path('sellers/<int:id>/update/inventory/<int:inventory_id>',UpdateInventoryItemsView.as_view(),name='update_inventory_items'),
    path('sellers/<int:id>/products',SellerProductsView.as_view(),name="seller_products"),
    path('sellers/<int:id>/add/variants/<int:product_id>',SellerAddVariantsView.as_view(),name="seller_products"),
    path('user/verification/<str:token>',TokenVerificationView.as_view(),name='email_verification_page'),
    path('users/profile/',UserProfileView.as_view(),name='profile_view'),
    path('users/profile/update',UserProfileUpdateView.as_view(),name='profile_update_view'),
    path('users/add/address',AddUserAddressView.as_view(),name='add_user_address'),
    path('users/address/update',UpdateUserAddressView.as_view(),name='update_user_address'),
    path('users/address/delete/<int:address_id>',DeleteUserAddressView.as_view(),name='delete_user_address'),
    path('dashboard',AdminDashboardView.as_view(),name='dashboard_view'),
]