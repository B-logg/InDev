from django.db import models

class Owner(models.Model):
    owner_id = models.AutoField(primary_key=True)  # PK
    name = models.CharField(max_length=100)  # 사장님 이름
    phone = models.CharField(max_length=20, blank=True, null=True)  # 선택적 연락처

    def __str__(self):
        return self.name