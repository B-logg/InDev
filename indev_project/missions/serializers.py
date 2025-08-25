# mission/serializers.py
from rest_framework import serializers
from .models import OwnerMission, CustomerDailyMission  # ServiceMission 제거

class OwnerMissionSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source="store.name", read_only=True)

    class Meta:
        model = OwnerMission
        fields = ["id", "store", "store_name", "content", "is_active", "customer", "created_at", "title", "reward"]

class OwnerMissionSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerMission
        fields = ["id", "title", "content", "reward", "is_active"]

class CustomerDailyMissionSerializer(serializers.ModelSerializer):
    owner_mission = OwnerMissionSimpleSerializer()

    class Meta:
        model = CustomerDailyMission
        fields = ["id", "assign_date", "status", "owner_mission"]
