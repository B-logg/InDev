# mission/models.py
from django.db import models
from django.utils import timezone
from customer.models import Customer
from store.models import Store

class OwnerMission(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)  # 더이상 사용 X
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    reward = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"[Owner] {self.store} - {self.content[:20]}"

# === 하루 배정 기록 ===
class CustomerDailyMission(models.Model):
    class Status(models.TextChoices):
        ASSIGNED = "ASSIGNED", "배정됨"
        COMPLETED = "COMPLETED", "완료"
        INVALIDATED = "INVALIDATED", "무효(다른 미션 완료됨)"
        EXPIRED = "EXPIRED", "만료(다음날)"

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="daily_missions")
    owner_mission = models.ForeignKey(OwnerMission, on_delete=models.CASCADE, related_name="assigned_entries")
    assign_date = models.DateField()  # 하루 단위
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ASSIGNED)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("customer", "assign_date", "owner_mission")
        indexes = [models.Index(fields=["customer", "assign_date"])]

    def complete(self):
        if self.status != self.Status.ASSIGNED:
            return
        self.status = self.Status.COMPLETED
        self.save(update_fields=["status"])
        # 같은 날 배정된 나머지 ASSIGNED → INVALIDATED
        (CustomerDailyMission.objects
            .filter(customer=self.customer, assign_date=self.assign_date, status=self.Status.ASSIGNED)
            .exclude(pk=self.pk)
            .update(status=self.Status.INVALIDATED))

    @staticmethod
    def expire_previous_days(customer, today=None):
        today = today or timezone.localdate()
        (CustomerDailyMission.objects
            .filter(customer=customer, assign_date__lt=today, status=CustomerDailyMission.Status.ASSIGNED)
            .update(status=CustomerDailyMission.Status.EXPIRED))
