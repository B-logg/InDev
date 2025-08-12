from django.db import models

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)  # PK
    name = models.CharField(max_length=100)  # 카테고리 이름

    def __str__(self):
        return self.name