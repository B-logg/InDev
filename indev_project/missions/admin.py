from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import OwnerMission,CustomerDailyMission
admin.site.register(OwnerMission)
admin.site.register(CustomerDailyMission)