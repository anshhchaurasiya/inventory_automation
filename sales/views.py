
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q, Sum, F, DecimalField, ExpressionWrapper
from django.shortcuts import render, get_object_or_404,redirect

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from inventory.models import Product

from sales.models import Cart
from sales.models import CartItem
from sales.models import Purchase
from sales.models import PurchaseItem

from sales.serializer import PurchaseSerializer,ProductSearchSerializer,AddToCartSerializer,CartItemSerializer,PurchaseItemSerializer, UpdateCartSerializer,CustomerDetailsSerializer,CheckoutSerializer

import json
from django.http import JsonResponse

@login_required()
def order_history(request):
    order_history=Purchase.objects.all().order_by("-purchase_date")
    return render(request,"sales/orders_history_page.html",{"order_history":order_history})

@login_required()
def order_details(request,purchase_id):
    order_details = get_object_or_404(
        Purchase.objects.prefetch_related('items__product'),
        id=purchase_id,
        user=request.user
    )

    return render(request, 'sales/order_details.html', {
        "order_details":order_details
    })


@login_required()
def address(request):
    print(float(request.GET.get('total')),"next",request.GET.get('total_quantity'))
    context={'total':request.GET.get('total'),
             'total_quantity':request.GET.get('total_quantity')}
    print(context)

    if request.method == "POST":
        data = json.loads(request.body)
        print(data,"data")
    #     return render(request, "sales/customer_form.html", context)

    return render(request, "sales/customer_form.html",context)

@login_required()
def invoice_page(request):
    return render(request, "sales/invoice.html")

# =====================================================
# HTML CART PAGE
# =====================================================

@login_required
def cart_page(request):
    return render(request, 'sales/cart.html')


# =====================================================
# PRODUCT SEARCH
# =====================================================

@api_view(['GET'])
@permission_classes([AllowAny])
def search_product(request):

    query = request.query_params.get('q', '').strip()

    if not query:
        return Response(
            {
                "status": "error",
                "message": "Please enter product name or SKU"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(sku__iexact=query)
    ).order_by('name').distinct()

    if not products.exists():
        return Response(
            {
                "status": "error",
                "message": "Product not found"
            },
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = ProductSearchSerializer(
        products,
        many=True
    )

    return Response(
        {
            "status": "success",
            "message": "Products found",
            "data": serializer.data
        },
        status=status.HTTP_200_OK
    )


# =====================================================
# ADD TO CART
# =====================================================
login_required
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):

    serializer = AddToCartSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {
                "status": "error",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    product_id = serializer.validated_data['product_id']
    quantity = serializer.validated_data['quantity']

    with transaction.atomic():

        # Create cart if it does not exist
        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        # Lock cart row
        cart = Cart.objects.select_for_update().get(
            pk=cart.pk
        )

        # Lock product row
        try:
            product = Product.objects.select_for_update().get(
                id=product_id
            )
        except Product.DoesNotExist:
            return Response(
                {
                    "status": "error",
                    "message": "Product not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if product.stock_quantity <= 0:
            return Response(
                {
                    "status": "error",
                    "message": "Product is out of stock"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Find existing cart item
        cart_item = CartItem.objects.select_for_update().filter(
            cart=cart,
            product=product
        ).first()

        if cart_item:

            new_quantity = cart_item.quantity + quantity

            if new_quantity > product.stock_quantity:
                return Response(
                    {
                        "status": "error",
                        "message": "Insufficient stock",
                        "available_stock": product.stock_quantity,
                        "cart_quantity": cart_item.quantity
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            cart_item.quantity = new_quantity
            cart_item.save(update_fields=['quantity'])

        else:

            if quantity > product.stock_quantity:
                return Response(
                    {
                        "status": "error",
                        "message": "Insufficient stock",
                        "available_stock": product.stock_quantity
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity
            )

    return Response(
        {
            "status": "success",
            "message": "Product added to cart",
            "product": product.name,
            "cart_quantity": cart_item.quantity
        },
        status=status.HTTP_200_OK
    )


# =====================================================
# GET CART
# =====================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):

    cart = Cart.objects.filter(
        user=request.user
    ).first()

    if not cart:
        return Response(
            {
                "status": "success",
                "message": "Cart is empty",
                "data": {
                    "items": [],
                    "total_amount": Decimal("0.00")
                }
            },
            status=status.HTTP_200_OK
        )

    cart_items = cart.items.select_related(
        'product'
    ).all()

    serializer = CartItemSerializer(
        cart_items,
        many=True
    )

    total_amount = cart_items.aggregate(
        total=Sum(
            ExpressionWrapper(
                F('quantity') * F('product__price'),
                output_field=DecimalField(
                    max_digits=20,
                    decimal_places=2
                )
            )
        )
    )['total'] or Decimal("0.00")

    return Response(
        {
            "status": "success",
            "message": "Cart retrieved successfully",
            "data": {
                "cart_id": cart.id,
                "items": serializer.data,
                "total_amount": total_amount
            }
        },
        status=status.HTTP_200_OK
    )


# =====================================================
# UPDATE CART ITEM
# =====================================================
login_required
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_cart_item(request, item_id):

    serializer = UpdateCartSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {
                "status": "error",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    quantity = serializer.validated_data['quantity']

    with transaction.atomic():

        # Only access the authenticated user's cart
        cart = Cart.objects.filter(
            user=request.user
        ).first()

        if not cart:
            return Response(
                {
                    "status": "error",
                    "message": "Cart not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        cart = Cart.objects.select_for_update().get(
            pk=cart.pk
        )

        # Restrict item lookup to this user's cart
        cart_item = CartItem.objects.select_for_update().filter(
            id=item_id,
            cart=cart
        ).first()

        if not cart_item:
            return Response(
                {
                    "status": "error",
                    "message": "Cart item not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        product = Product.objects.select_for_update().get(
            id=cart_item.product_id
        )

        if quantity > product.stock_quantity:
            return Response(
                {
                    "status": "error",
                    "message": "Insufficient stock",
                    "available_stock": product.stock_quantity
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item.quantity = quantity

        cart_item.save(
            update_fields=['quantity']
        )

        subtotal = quantity * product.price

    return Response(
        {
            "status": "success",
            "message": "Cart quantity updated",
            "product": product.name,
            "quantity": quantity,
            "subtotal": subtotal
        },
        status=status.HTTP_200_OK
    )


# =====================================================
# REMOVE CART ITEM
# =====================================================

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_cart_item(request, item_id):

    with transaction.atomic():

        cart = Cart.objects.filter(
            user=request.user
        ).first()

        if not cart:
            return Response(
                {
                    "status": "error",
                    "message": "Cart not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        cart = Cart.objects.select_for_update().get(
            pk=cart.pk
        )

        cart_item = CartItem.objects.select_for_update().filter(
            id=item_id,
            cart=cart
        ).first()

        if not cart_item:
            return Response(
                {
                    "status": "error",
                    "message": "Cart item not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        product_name = cart_item.product.name

        cart_item.delete()

    return Response(
        {
            "status": "success",
            "message": "Product removed from cart",
            "product": product_name
        },
        status=status.HTTP_200_OK
    )


# =====================================================
# CHECKOUT
# =====================================================
login_required
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout(request):
    # print(request.data)
    print(dict(request.session))
    serializer = CheckoutSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {
                "status": "error",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    if not serializer.validated_data.get('confirm_checkout', True):
        return Response(
            {
                "status": "error",
                "message": "Checkout was not confirmed"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    with transaction.atomic():

        cart = Cart.objects.filter(
            user=request.user
        ).first()

        if not cart:
            return Response(
                {
                    "status": "error",
                    "message": "Cart not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        cart = Cart.objects.select_for_update().get(
            pk=cart.pk
        )

        cart_items = list(
            CartItem.objects.select_for_update()
            .filter(cart=cart)
            .order_by('product_id')
        )

        if not cart_items:
            return Response(
                {
                    "status": "error",
                    "message": "Your cart is empty"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Lock all required product rows in a consistent order
        product_ids = [
            item.product_id for item in cart_items
        ]

        products = Product.objects.select_for_update().filter(
            id__in=product_ids
        ).order_by('id')

        product_map = {
            product.id: product for product in products
        }

        total_amount = Decimal("0.00")
        purchase_items = []

        # Validate stock and calculate total
        for item in cart_items:

            product = product_map.get(item.product_id)

            if not product:
                return Response(
                    {
                        "status": "error",
                        "message": "A product in your cart no longer exists"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if item.quantity > product.stock_quantity:
                return Response(
                    {
                        "status": "error",
                        "message": "Insufficient stock during checkout",
                        "product": product.name,
                        "requested_quantity": item.quantity,
                        "available_stock": product.stock_quantity
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            unit_price = product.price

            subtotal = unit_price * item.quantity

            total_amount += subtotal

            purchase_items.append(
                {
                    "product": product,
                    "quantity": item.quantity,
                    "unit_price": unit_price
                }
            )

        # Create purchase
        purchase = Purchase.objects.create(
            user=request.user,
            total_amount=total_amount,
            status='Completed'
        )

        # Create purchase items and deduct stock
        purchase_item_objects = []

        for item_data in purchase_items:

            product = item_data['product']

            product.stock_quantity -= item_data['quantity']

            product.save(
                update_fields=['stock_quantity']
            )

            purchase_item_objects.append(
                PurchaseItem(
                    purchase=purchase,
                    product=product,
                    quantity=item_data['quantity'],
                    unit_price=item_data['unit_price']
                )
            )

        PurchaseItem.objects.bulk_create(
            purchase_item_objects
        )

        # Clear cart only after successful purchase creation
        CartItem.objects.filter(
            cart=cart
        ).delete()
    data=request.data
    print(data)
    customer_details_serialzer=CustomerDetailsSerializer(data=data)
    if customer_details_serialzer.is_valid():
        customer_details_serialzer.save(purchase=purchase)
    else:
        return Response(
                    {
                        "status": "error",
                        "errors": serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
    purchase_serializer = PurchaseSerializer(purchase)
    data=json.loads(request.body)
    data=dict(purchase_serializer.data)|data
    # print(data)


    return Response(
        {
            "status": "success",
            "message": "Purchase created successfully",
            # "data": purchase_serializer.data
            'data':data
        },
        status=status.HTTP_201_CREATED
    )


# =====================================================
# PURCHASE HISTORY
# =====================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def purchase_history(request):

    purchases = Purchase.objects.filter(
        user=request.user
    ).prefetch_related(
        'items__product'
    ).order_by('-purchase_date')

    serializer = PurchaseSerializer(
        purchases,
        many=True
    )
    return Response(
        {
            "status": "success",
            "message": "Purchase history retrieved successfully",
            "data": serializer.data
        },
        status=status.HTTP_200_OK
    )


# =====================================================
# PURCHASE DETAILS
# =====================================================
# not using this code  (below)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def purchase_detail(request, purchase_id):

    purchase = get_object_or_404(
        Purchase.objects.prefetch_related('items__product'),
        id=purchase_id,
        user=request.user
    )

    serializer = PurchaseSerializer(purchase)

    return Response(
        {
            "status": "success",
            "message": "Purchase details retrieved successfully",
            "data": serializer.data
        },
        status=status.HTTP_200_OK
    )
