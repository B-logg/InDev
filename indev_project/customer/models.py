from django.db import models

# Create your models here.
class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=50)
    intro = models.TextField(blank=True, null=True)
    reward = models.IntegerField(default=0)

    