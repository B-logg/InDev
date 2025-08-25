from django.db import models
from route.models import Routine
from customer.models import Customer
from store.models import Store

# Create your models here.
class PostMassil(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    neighborhood = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = image = models.ImageField(upload_to="post_images/", null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="posts", null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="posts", null=True, blank=True)
    
    routine = models.OneToOneField(Routine, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        if self.customer:
            return f"Post #{self.title} by Customer {self.customer.nickname}"
        elif self.store:
            return f"Post #{self.title} by Store {self.store.store_name}"
        return f"Post #{self.title} (Unknown author)"
