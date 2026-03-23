from django.db import models
from django.conf import settings
from food.models import Food

class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_price = models.FloatField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    food = models.ForeignKey(Food,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)