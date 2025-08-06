from django.db import models
from customer.models import Customer

class Routine(models.Model):
    routine_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"Routine: {self.title}"
    
class VisitRoutine(models.Model):
    VisitRoutine_id = models.AutoField(primary_key=True)
    order_index = models.IntegerField()
    lat = models.FloatField() # 위도
    lng = models.FloatField() # 경도

    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name='visit_points')

    def __str__(self):
        return f"{self.order_index} ({self.lat}, {self.long})"
    


