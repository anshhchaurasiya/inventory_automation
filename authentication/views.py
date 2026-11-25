from django.http import HttpResponse
from authentication.serializers import RegisterSerializer
from django.contrib.auth import authenticate, login as auth_login, logout 
from django.contrib.auth.decorators import login_required
from authentication.models import CustomUser
from django.shortcuts import render,redirect





def register_view(request):

    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect('cart-page')
        print(serializer.errors)
        # print(request.POST)
        form_data=request.POST.copy()
        form_data.pop('password', None)
        form_data.pop('confirm_password', None)
        return render(request, 'authentication/registration.html',{ 'errors': serializer.errors,
                'form_data': form_data})

    else:
        return render(request, 'authentication/registration.html')

def login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user = authenticate(request, email=email, password=password) 
        if user is not None:
            auth_login(request, user)
            return redirect("cart-page")
        else:
            return render(request, 'authentication/login.html',context={"error":"Invalid email or password",
                                                                        "email":email})
    else:
        return render(request, 'authentication/login.html')

@login_required()
def logout_view(request):
    logout(request)
    return HttpResponse("You have been logged out successfully")
