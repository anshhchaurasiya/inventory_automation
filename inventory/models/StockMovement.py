from django.db import models
from django.utils import timezone

class StockMovement(models.Model):
    
    MOVEMENT_CHOICES = [
        ('IN', 'In'),
        ('OUT', 'Out'),
        ('ADJUSTMENT', 'Adjustment'),
    ]

    product = models.ForeignKey(
        'Product', 
        on_delete=models.CASCADE, 
        related_name='stock_movements'
    )
    movement_type = models.CharField(
        max_length=10, 
        choices=MOVEMENT_CHOICES
    )
    quantity = models.IntegerField()
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'Stock_Movement'

    def __str__(self):
        return f"{self.movement_type} - {self.product.name} ({self.quantity})"

