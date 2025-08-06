from django.db import models
from route.models import Routine

# Create your models here.
class PostMassil(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    routine = models.OneToOneField(Routine, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Post #{self.title}"
