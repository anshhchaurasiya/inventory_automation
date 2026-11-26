
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

from sales.serializer import PurchaseSerializer,ProductSearchSerializer,AddToCartSerializer,CartItemSerializer,PurchaseItemSerializer
from sales.serializer import UpdateCartSerializer,CustomerDetailsSerializer,CheckoutSerializer

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
