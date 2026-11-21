from django.db import models
from django.conf import settings

PURCHASE_STATUS_CHOICES  = (
    ('pending', 'Pending'),
    ('completed','Completed'),
    ('cancelled','Cancelled'),
    )

class Purchase(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='purchases'
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    purchase_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=PURCHASE_STATUS_CHOICES,
        default='pending'
    )
    
    class Meta:
        db_table = 'Purchases'
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'

    def __str__(self):
        return f"Purchase #{self.id}"