from django.db import models

CUSTOMER_TYPE_CHOICES = (
    ('Individual', 'Individual'),
    ('Business', 'Business'),
)

PAYMENT_METHOD_CHOICES = (
    ('COD', 'Cash on Delivery'),
    ('UPI', 'UPI'),
    ('Card', 'Card'),
    ('Bank Transfer', 'Bank Transfer'),
)

class CustomerDetails(models.Model):
    id=models.AutoField(primary_key=True)
    purchase = models.OneToOneField(
        'sales.Purchase',
        on_delete=models.CASCADE,
        related_name='checkout_details'
    )
    customer_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    customer_type = models.CharField(
        max_length=20,
        choices=CUSTOMER_TYPE_CHOICES,
        default='Individual'
    )
    company_name = models.CharField(max_length=200, null=True, blank=True)
    gstin = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='COD'
    )
    notes = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'CustomerDetails'
        verbose_name = 'Customer Detail'
        verbose_name_plural = 'Customer Details'

    def save(self,*args,**kwargs):
        if self.company_name is not None and self.company_name.strip() == '':
            self.company_name=None
        if self.gstin is not None and self.gstin.strip() == '':
            self.gstin = None
        if self.notes is not None and self.notes.strip() == '':
            self.notes = None
        super().save(*args, **kwargs)
