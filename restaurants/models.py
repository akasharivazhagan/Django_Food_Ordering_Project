from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Food(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name