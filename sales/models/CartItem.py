from django.db import models
from django.core.validators import MinValueValidator

class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(
        'sales.Cart',
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        'inventory.Product',
        on_delete=models.CASCADE,
        related_name='cart_items'
    )

    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'CartItems'
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

        constraints = [
            models.UniqueConstraint(
                fields=['cart', 'product'],
                name='unique_product_per_cart'
            )
        ]

    def __str__(self):
        return f"{self.product} - {self.quantity}"