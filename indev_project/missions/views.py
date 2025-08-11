# mission/views.py
from django.db.models.functions import Random
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from customer.models import Customer
from .models import ServiceMission, OwnerMission
from .serializers import ServiceMissionSerializer, OwnerMissionSerializer

# -----------------------------
# ServiceMission CRUD
# -----------------------------
class ServiceMissionListCreateView(generics.ListCreateAPIView):
    queryset = ServiceMission.objects.all()
    serializer_class = ServiceMissionSerializer

class ServiceMissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceMission.objects.all()
    serializer_class = ServiceMissionSerializer


# -----------------------------
# OwnerMission CRUD
# -----------------------------
class OwnerMissionListCreateView(generics.ListCreateAPIView):
    queryset = OwnerMission.objects.all()
    serializer_class = OwnerMissionSerializer

class OwnerMissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OwnerMission.objects.all()
    serializer_class = OwnerMissionSerializer


# -----------------------------
# Assign Missions (랜덤 배정 & 고정)
# -----------------------------
class AssignMissionsView(APIView):
    """
    GET /mission/customers/<pk>/missions/assign/
    """
    def get(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response({"detail": "해당 고객이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 1) 서비스 미션 (고객이 이미 있으면 유지)
        service = ServiceMission.objects.filter(customer=customer).first()
        if not service:
            service = ServiceMission.objects.filter(is_active=True, customer__isnull=True).order_by(Random()).first()
            if service:
                service.customer = customer
                service.save()

        # 2) 오너 미션 (고객이 이미 있으면 유지)
        owners = OwnerMission.objects.filter(customer=customer)
        if owners.count() < 2:
            needed = 2 - owners.count()
            available = OwnerMission.objects.filter(is_active=True, customer__isnull=True).order_by(Random())[:needed]
            for om in available:
                om.customer = customer
                om.save()
            owners = OwnerMission.objects.filter(customer=customer)

        return Response({
            "service_mission": ServiceMissionSerializer(service).data if service else None,
            "owner_missions": OwnerMissionSerializer(owners, many=True).data
        }, status=status.HTTP_200_OK)
