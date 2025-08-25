# mission/views.py
from django.db import transaction
from django.db.models.functions import Random
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from customer.models import Customer
from .models import OwnerMission, CustomerDailyMission
from .serializers import (
    OwnerMissionSerializer,
    CustomerDailyMissionSerializer,
)

ASSIGN_COUNT = 3

# OwnerMission CRUD 그대로 유지
class OwnerMissionListCreateView(generics.ListCreateAPIView):
    queryset = OwnerMission.objects.all()
    serializer_class = OwnerMissionSerializer

class OwnerMissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OwnerMission.objects.all()
    serializer_class = OwnerMissionSerializer


class AssignMissionsView(APIView):
    """
    GET /mission/customer/<pk>/
    - 오늘자 배정이 없으면: 어제까지 ASSIGNED → EXPIRED, 랜덤 3개 ASSIGNED 생성
    - 이미 오늘자 배정이 있으면 그대로 반환
    """
    def get(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response({"detail": "해당 고객이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        today = timezone.localdate()
        with transaction.atomic():
            # 어제까지 미완료(ASSIGNED) 항목은 만료 처리
            CustomerDailyMission.expire_previous_days(customer, today=today)

            today_qs = CustomerDailyMission.objects.select_for_update().filter(
                customer=customer, assign_date=today
            )

            if today_qs.count() == 0:
                # 활성 미션 중 랜덤 3개
                available = (OwnerMission.objects
                             .filter(is_active=True)
                             .order_by(Random())[:ASSIGN_COUNT])

                to_create = [
                    CustomerDailyMission(
                        customer=customer,
                        owner_mission=om,
                        assign_date=today,
                        status=CustomerDailyMission.Status.ASSIGNED,
                    )
                    for om in available
                ]
                CustomerDailyMission.objects.bulk_create(to_create)
                today_qs = CustomerDailyMission.objects.filter(customer=customer, assign_date=today)

        data = CustomerDailyMissionSerializer(today_qs, many=True).data
        return Response({"date": str(today), "count": len(data), "missions": data}, status=status.HTTP_200_OK)


class CompleteMissionView(APIView):
    """
    POST /mission/customer/<pk>/complete/<mission_id>/
    - 오늘 배정된 해당 미션을 완료 처리
    - 같은 날 다른 ASSIGNED는 전부 INVALIDATED
    """
    def post(self, request, pk, mission_id):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response({"detail": "해당 고객이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        today = timezone.localdate()
        try:
            entry = CustomerDailyMission.objects.get(
                customer=customer,
                assign_date=today,
                owner_mission_id=mission_id
            )
        except CustomerDailyMission.DoesNotExist:
            return Response({"detail": "오늘 배정된 해당 미션이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        if entry.status != CustomerDailyMission.Status.ASSIGNED:
            return Response({"detail": f"현재 상태가 '{entry.status}'라 완료 처리 불가합니다."},
                            status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            entry.complete()

        today_qs = CustomerDailyMission.objects.filter(customer=customer, assign_date=today)
        return Response({
            "date": str(today),
            "missions": CustomerDailyMissionSerializer(today_qs, many=True).data
        }, status=status.HTTP_200_OK)
