from django.contrib import admin
from .models import Character

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ("character_id", "name")  # 원하는 필드 표시

from .models import Customer
admin.site.register(Customer)