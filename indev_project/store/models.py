# store/models.py
from django.db import models

class Store(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# missions 테스트를 위해 store_id 가 필요해서 임시로 만든 model입니다
# 나중에 필요하시면 바꾸셔도 상관없습니다!