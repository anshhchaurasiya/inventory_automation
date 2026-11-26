
from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register_view, name='register'),
    path ('login/',views.login, name='login'),
    path ('logout/', views.logout_view, name='logout'),
]