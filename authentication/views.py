from django.http import HttpResponse
from authentication.serializers import RegisterSerializer
from django.contrib.auth import authenticate, login as auth_login, logout 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from authentication.models import CustomUser




def register_view(request):

    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse("User created successfully")

        return HttpResponse(serializer.errors)

    else:
        return render(request, 'authentication/registration.html')

def login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user = authenticate(request, email=email, password=password) 
        if user is not None:
            auth_login(request, user)
            return HttpResponse("Login successful")
        else:
            return HttpResponse("Invalid credentials")
    else:
        return render(request, 'authentication/login.html')

@login_required()
def logout_view(request):
    logout(request)
    return HttpResponse("You have been logged out successfully")
