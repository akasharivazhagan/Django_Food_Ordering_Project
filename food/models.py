from django.db import models

class Food(models.Model):
    #id is i don't write but django autometically create the field in DB
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    price = models.FloatField()