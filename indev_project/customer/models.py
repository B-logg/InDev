from django.db import models


# Create your models here.
class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=50)
    intro = models.TextField(blank=True, null=True)
    reward = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # character = models.ForeignKey('Character', on_delete=models.SET_NULL, null=True, blank=True, related_name='customers')
    
    def __str__(self):
        return self.nickname

class Character(models.Model):
    character_id = models.AutoField(primary_key=True)  # PK
    name = models.CharField(max_length=100)  # 캐릭터 이름
    image = models.ImageField(upload_to='character/', blank=True, null=True)  # 캐릭터 이미지

    def __str__(self):
        return self.name