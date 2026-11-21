from django.db import models


class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    alternate_phone_number = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(max_length=100)
    gst_number = models.CharField(max_length=15)
    address = models.TextField()



    class Meta:
        # Set your custom table name here
        db_table = 'Supplier'

    def __str__(self):
        return self.name