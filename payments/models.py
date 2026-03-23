from django.db import models
from orders.models import Order

class Payment(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    amount = models.FloatField()
    status = models.CharField(max_length=20)