from django.core.checks import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from inventory import models
from inventory.models import Product, Category, Supplier, StockMovement
from inventory.serializer import ProductSerializer, AddExistingProductSerializer

class ProductView(View):
    # List products or render add page
    def get(self, request):
        if request.path.endswith('/add/'):
            categories = Category.objects.all()
            suppliers = Supplier.objects.all()
            return render(request, 'inventory/product/product_add.html', {
                'categories': categories,
                'suppliers': suppliers
            })
        name = request.GET.get('name', '').strip()
        sku = request.GET.get('sku', '').strip().upper()
        supplier = request.GET.get('supplier', '').strip()

        products = Product.objects.select_related(
            'category', 'supplier'
        ).all()

        if name:
            products = products.filter(name__icontains=name)

        if sku:
            products = products.filter(sku__icontains=sku)

        if supplier:
            products = products.filter(supplier__name__icontains=supplier)  
                    

        return render(request, 'inventory/product/product_list.html', {
            'products': products
        })

    # Add product
    def post(self, request):
        data = request.POST
        serializer = ProductSerializer(data=data)
        reason = data.get('Reason', 'Initial stock')  # Default reason if not provided
        if reason is None or reason.strip() == '':
            reason = 'Initial stock'  # Set default reason if empty
        if serializer.is_valid():
            product=serializer.save()
            StockMovement.objects.create(
            product=product,  # Assuming you want to create a stock movement for the first product
            movement_type='IN',
            quantity=product.stock_quantity,
            reason=reason
        )
            return render(request, 'inventory/product/product_add.html', {
            'success': f"Successfully added {product.stock_quantity} items to stock for {product.name}."
        })

        # If invalid, re-render form with errors and dropdown data
        categories = Category.objects.all()
        suppliers = Supplier.objects.all()
        return render(request, 'inventory/product/product_add.html', {
            'errors': serializer.errors,
            'categories': categories,
            'suppliers': suppliers,
            'form_data': request.POST
        })



# adding existing produuct
def add_existing_product(request):

    if request.method == 'POST':

        data = request.POST
        serializer = AddExistingProductSerializer(data=data)
        
        reason = data.get('Reason', 'Initial stock')  
        if reason is None or reason.strip() == '':
            reason = 'Initial stock'  # Set default reason if empty
        if serializer.is_valid():

            sku = serializer.validated_data['sku']
            quantity = serializer.validated_data['additional_quantity']

            product = Product.objects.get(sku=sku)
            product.stock_quantity += quantity
            product.save()

            StockMovement.objects.create(
            product=product,  # Assuming you want to create a stock movement for the first product
            movement_type='IN',
            quantity=quantity,
            reason=reason
        )

            return render(request, 'inventory/product/add_existing_product.html', {
                'success': f"Successfully added {quantity} items to stock for {product.name}."
            })

        return render(request, 'inventory/product/add_existing_product.html', {
            'errors': serializer.errors
        })

    return render(request, 'inventory/product/add_existing_product.html')