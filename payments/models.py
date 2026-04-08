from django.db import models
from orders.models import Order

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=200)
    razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=50, default='created')

    def __str__(self):
        return self.razorpay_order_id