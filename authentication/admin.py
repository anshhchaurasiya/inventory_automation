from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from authentication.models import CustomUser
from authentication.forms import (
    CustomUserCreationForm,
    CustomUserChangeForm
)


class CustomUserAdmin(UserAdmin):

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = (
        'id',
        'email',
        'first_name',
        'last_name',
        'role',
        'phone_number',
        'is_active',
    )

    list_filter = ('role', 'is_active', 'is_staff')

    search_fields = ('email', 'first_name', 'last_name')

    ordering = ('id',)

    filter_horizontal = ('groups', 'user_permissions')

    fieldsets = (
        ('Login Information', {
            'fields': ('email', 'password')
        }),

        ('Personal Information', {
            'fields': (
                'first_name',
                'last_name',
                'phone_number',
                'role',
            )
        }),

        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),

        ('Important Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'phone_number',
                'role',
                'password1',
                'password2',
                'is_active',
                'is_staff',
            ),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)