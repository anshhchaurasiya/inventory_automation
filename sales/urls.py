
from django.urls import path
from . import views


urlpatterns = [

    # HTML FRONTEND
    path(
        'cart-page/',
        views.cart_page,
        name='cart-page'
    ),

    # PRODUCT SEARCH
    path(
        'search/',
        views.search_product,
        name='search-product'
    ),

    # CART OPERATIONS
    path(
        'cart/add/',
        views.add_to_cart,
        name='add-to-cart'
    ),

    path(
        'cart/',
        views.get_cart,
        name='get-cart'
    ),

    path(
        'cart/update/<int:item_id>/',
        views.update_cart_item,
        name='update-cart-item'
    ),

    path(
        'cart/remove/<int:item_id>/',
        views.remove_cart_item,
        name='remove-cart-item'
    ),

    # CHECKOUT
    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),
    path('customer-details/',views.customer_details,name='customer_details'),
    path('invoice/',views.invoice_page,name="invoice"),
    path('orders/', views.order_history, name='order_history'),
    path('orders/<int:purchase_id>/', views.order_details, name='order_details'),
]
