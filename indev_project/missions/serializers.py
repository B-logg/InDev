# mission/serializers.py
from rest_framework import serializers
from .models import ServiceMission, OwnerMission

class ServiceMissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceMission
        fields = ["id", "content", "is_active", "customer", "created_at"]

class OwnerMissionSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source="store.name", read_only=True)  # 가게 이름 같이 제공

    class Meta:
        model = OwnerMission
        fields = ["id", "store", "store_name", "content", "is_active", "customer", "created_at", "title", "reward"]
