from django.db import models


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    sku=models.CharField(max_length=100, unique=True)
    category=models.ForeignKey('Category', on_delete=models.PROTECT, related_name='products')
    supplier=models.ForeignKey('Supplier', on_delete=models.PROTECT, related_name='products')
    price=models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity=models.IntegerField(default=0)




    class Meta:
        # Set your custom table name here
        db_table = 'Product'

    def __str__(self):
        return self.name