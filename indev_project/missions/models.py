# mission/models.py
from django.db import models
from customer.models import Customer
from store.models import Store

class ServiceMission(models.Model):
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[Service] {self.content[:20]}"

class OwnerMission(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE,null=True,blank=True)  # 어떤 가게의 미션인지
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    reward = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"[Owner] {self.store} - {self.content[:20]}"
