from django.db import models
from django.core.validators import MinValueValidator

class PurchaseItem(models.Model):
    id = models.AutoField(primary_key=True)
    purchase = models.ForeignKey(
        'sales.Purchase',
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        'inventory.Product',
        on_delete=models.PROTECT,
        related_name='purchase_items'
    )

    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    @property
    def subtotal(self):
        return self.quantity * self.unit_price    

    class Meta:
        db_table = 'PurchaseItems'
        verbose_name = 'Purchase Item'
        verbose_name_plural = 'Purchase Items'

    def __str__(self):
        return f"{self.product} - {self.quantity}"