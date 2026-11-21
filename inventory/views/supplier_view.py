from django.http import request
from rest_framework.views import APIView, View

from inventory.models import Supplier
from inventory.serializer import SupplierSerializer

from django.shortcuts import get_object_or_404, render, redirect


class SupplierView(View):

    # Get all suppliers
    def get(self, request):
        if request.path.endswith('/add/'):
            return render(request, 'inventory/Supplier/supplier_add.html')
        
        suppliers = Supplier.objects.all()
        serializer = SupplierSerializer(suppliers, many=True)
        

        return render(
            request,
            'inventory/Supplier/supplier_list.html',
            {'suppliers': serializer.data}
        )

    # Add supplier
    def post(self, request):
        name=request.POST.get('name')
        phone_number=request.POST.get('phone_number')
        alternate_phone_number=request.POST.get('alternate_phone_number')
        email=request.POST.get('email')
        gst_number=request.POST.get('gst_number')
        address=request.POST.get('address')
        dict_data = {
            'name': name,
            'phone_number': phone_number,
            'alternate_phone_number': alternate_phone_number,
            'email': email,
            'gst_number': gst_number,
            'address': address
        }
        print(dict_data)
        serializer = SupplierSerializer(data=dict_data)

        if serializer.is_valid():
            serializer.save()
            return redirect('supplier-list')
        else:
            print(serializer.errors)
        return render(
            request,
            'inventory/Supplier/supplier_add.html',
            {'errors': serializer.errors}
        )


class SupplierDetailView(View):

    

    def get(self, request, pk):

        supplier = get_object_or_404(Supplier, pk=pk)

        return render(
            request,
            'inventory/Supplier/supplier_detail.html',
            {'supplier': supplier}
        )

    def post(self, request, pk):

        supplier = get_object_or_404(Supplier, pk=pk)

        # Delete supplier
        if request.POST.get('action') == 'delete':

            supplier.delete()

            return redirect('supplier-list')

        # Update supplier
        serializer = SupplierSerializer(
            supplier,
            data=request.POST
        )

        if serializer.is_valid():

            serializer.save()

            return redirect('supplier-detail', pk=supplier.id)

        return render(
            request,
            'inventory/Supplier/supplier_detail.html',
            {
                'supplier': supplier,
                'errors': serializer.errors,
                'form_data': request.POST
            }
        )