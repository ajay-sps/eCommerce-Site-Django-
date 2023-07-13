from django.urls import path
from orders.views import AddItemsToUserCartView,UserCartView,DeleteUserCartItemView,AddItemsToUserWishlistView,DeleteFromUserWishlistView,UserWishlistView,UpdateCartItems,UserCartCheckOutView,UserOrderPlacedView,UserProductCheckoutView,UserOrdersView,UserOrdersDetailView


urlpatterns = [
    path('users/<int:user_id>/cart',UserCartView.as_view(),name='user_cart'),
    path('users/<int:user_id>/cart/add',AddItemsToUserCartView.as_view(),name='add_items_in_cart'),
    path('users/<int:user_id>/cart/delete/<int:item_id>',DeleteUserCartItemView.as_view(),name="delete_cart_item"),
    path('users/<int:user_id>/cart/update/',UpdateCartItems.as_view(),name='update_cart_items'),
    path('users/<int:user_id>/wishlist/add',AddItemsToUserWishlistView.as_view(),name='add_items_in_wishlist'),
    path('users/<int:user_id>/wishlist/delete',DeleteFromUserWishlistView.as_view(),name='remove_items_from_wishlist'),
    path('users/wishlist/',UserWishlistView.as_view(),name='user_wishlist_view'),
    path('users/<int:id>/checkout',UserCartCheckOutView.as_view(),name='user_cart_checkout'),
    path('users/<int:id>/product/checkout',UserProductCheckoutView.as_view(),name='user_product_checkout'),
    path('users/<int:id>/orderplaced/',UserOrderPlacedView.as_view(),name='user_order_placed'),
    path('users/<int:id>/orders',UserOrdersView.as_view(),name=('user_orders')),
    path('users/<int:id>/order/details',UserOrdersDetailView.as_view(),name='user_order_detail_view'),
]