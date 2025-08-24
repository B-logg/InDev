from django.db import models
from route.models import Routine
from customer.models import Customer

# Create your models here.
class PostMassil(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    neighborhood = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = image = models.ImageField(upload_to="post_images/", null=True, blank=True)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="posts", null=True, blank=True)
    routine = models.OneToOneField(Routine, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Post #{self.title} by {self.user.nickname if self.user else 'Unknown'}"
