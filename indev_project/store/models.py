# store/models.py
from django.db import models
from customer.models import Character

class Store(models.Model):
    store_id = models.AutoField(primary_key=True)  # PK
    name = models.CharField(max_length=200)  # 가게 이름
    open_date = models.DateField(null=True)  # 오픈 날짜
    intro = models.TextField(blank=True, null=True)  # 가게 소개
    address = models.CharField(max_length=300, default=' ')  # 주소

    category = models.ForeignKey('category.Category', on_delete=models.SET_NULL, 
        null=True, db_column="Category_id")

    character = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True, blank=True, related_name='stores')


    def __str__(self):
        return self.name

class Analysis(models.Model):
    analysis_id = models.AutoField(primary_key=True)  # PK
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE, db_column="store_id")
    data = models.URLField()  # 가게 데이터 분석 자료 URL

    def __str__(self):
        return f"Analysis for {self.store.name}"