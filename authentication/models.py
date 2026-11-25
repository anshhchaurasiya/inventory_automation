from django.contrib.auth.models import AbstractUser
from django.db import models

from authentication.user_manager import CustomUserManager


Role_choices = (
    ('Admin', 'Admin'),
    ('Manager','Manager'),
    ('Staff','Staff'),
    )

class CustomUser(AbstractUser):
    phone_number = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )
    username = None
    email = models.EmailField(unique=True, blank=False, null=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 
    role=models.CharField(max_length=20, choices=Role_choices, default='Staff')
    objects = CustomUserManager()

    class Meta:
        # Set your custom table name here
        db_table = 'Users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username