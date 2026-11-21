from django.urls import path
from inventory.views import SupplierView, SupplierDetailView
from inventory.views.product_view import ProductView, add_existing_product

urlpatterns = [
    path('suppliers/', SupplierView.as_view(), name='supplier-list'),
    path('suppliers/add/', SupplierView.as_view(), name='supplier-add'),
    path('suppliers/<int:pk>/', SupplierDetailView.as_view(), name='supplier-detail'),

    path('products/', ProductView.as_view(), name='product-list'),
    path('products/add/', ProductView.as_view(), name='product-add'),
    path('products/add-existing/', add_existing_product, name='add-existing-product'),
]