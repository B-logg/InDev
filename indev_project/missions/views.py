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
S = CustomerDailyMission.Status

# OwnerMission CRUD 그대로 유지
class OwnerMissionListCreateView(generics.ListCreateAPIView):
    queryset = OwnerMission.objects.all()
    serializer_class = OwnerMissionSerializer

class OwnerMissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OwnerMission.objects.all()
    serializer_class = OwnerMissionSerializer



class OwnerMissionByStoreListView(generics.ListAPIView):
    serializer_class = OwnerMissionSerializer
    def get_queryset(self):
        store_id = self.kwargs.get("store_id")
        return OwnerMission.objects.filter(store_id=store_id).order_by("-created_at")

class AssignMissionsView(APIView):
    """
    GET /mission/assign/<pk>/
    - 오늘자 배정이 없으면: 어제까지 ASSIGNED/ING → EXPIRED, 랜덤 3개 ASSIGNED 생성
    - 이미 오늘자 배정이 있으면 그대로 반환
    """
    def get(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response({"detail": "해당 고객이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        today = timezone.localdate()
        with transaction.atomic():
            # ✅ 어제까지 'ASSIGNED'와 'ING' 모두 만료 처리
            (CustomerDailyMission.objects
                .select_for_update()
                .filter(customer=customer, assign_date__lt=today, status__in=[S.ASSIGNED, S.ING])
                .update(status=S.EXPIRED))

            today_qs = CustomerDailyMission.objects.select_for_update().filter(
                customer=customer, assign_date=today
            )

            if today_qs.count() == 0:
                available = (OwnerMission.objects
                             .filter(is_active=True)
                             .order_by(Random())[:ASSIGN_COUNT])

                to_create = [
                    CustomerDailyMission(
                        customer=customer,
                        owner_mission=om,
                        assign_date=today,
                        status=S.ASSIGNED,
                    )
                    for om in available
                ]
                CustomerDailyMission.objects.bulk_create(to_create)
                today_qs = CustomerDailyMission.objects.filter(customer=customer, assign_date=today)

        data = CustomerDailyMissionSerializer(today_qs, many=True).data
        return Response({"date": str(today), "count": len(data), "missions": data}, status=status.HTTP_200_OK)


# mission/views.py

S = CustomerDailyMission.Status

class StartMissionView(APIView):
    """
    POST /mission/assign/<pk>/start/<mission_id>/
    - 오늘 배정된 미션을 'ING(진행중)'으로 표시
    - 같은 날 다른 'ING'는 'ASSIGNED'로 되돌려 하루에 하나만 진행중 유지
    - ING 로 바뀐 미션의 OwnerMission.is_active = False
    - 🔹 (추가) 기존 ING -> ASSIGNED 로 되돌아간 미션들의 OwnerMission.is_active = True
    """
    def post(self, request, pk, mission_id):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response({"detail": "해당 고객이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        today = timezone.localdate()
        with transaction.atomic():
            qs_today = CustomerDailyMission.objects.select_for_update().filter(
                customer=customer, assign_date=today
            )
            try:
                entry = qs_today.get(owner_mission_id=mission_id)
            except CustomerDailyMission.DoesNotExist:
                return Response({"detail": "오늘 배정된 해당 미션이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

            if entry.status == S.ASSIGNED:
                # ⬇️ 기존에 진행중이던 것(있다면) 수집
                prev_ing_entries = list(
                    qs_today.filter(status=S.ING).exclude(pk=entry.pk).only("owner_mission_id")
                )

                # 기존 ING → ASSIGNED
                qs_today.filter(status=S.ING).exclude(pk=entry.pk).update(status=S.ASSIGNED)

                # ⬇️ 기존 ING 였던 미션들 다시 활성화
                if prev_ing_entries:
                    OwnerMission.objects.filter(
                        pk__in=[e.owner_mission_id for e in prev_ing_entries]
                    ).update(is_active=True)

                # 이번 것을 진행중으로 + 비활성화
                entry.status = S.ING
                entry.save(update_fields=["status"])
                OwnerMission.objects.filter(pk=entry.owner_mission_id).update(is_active=False)

            elif entry.status == S.ING:
                # 멱등성: 이미 진행중이면 상태 유지, 비활성화만 보정
                OwnerMission.objects.filter(pk=entry.owner_mission_id).update(is_active=False)

            else:
                return Response(
                    {"detail": f"현재 상태가 '{entry.status}'라 시작할 수 없습니다."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            data = CustomerDailyMissionSerializer(qs_today, many=True).data
            return Response({"date": str(today), "missions": data}, status=status.HTTP_200_OK)

class CompleteMissionView(APIView):
    """
    POST /mission/assign/<pk>/complete/<mission_id>/
    - 오늘 배정된 해당 미션을 'COMPLETED'
    - 같은 날의 나머지 'ASSIGNED'와 'ING'는 모두 'INVALIDATED'
    """
    def post(self, request, pk, mission_id):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response({"detail": "해당 고객이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        today = timezone.localdate()
        with transaction.atomic():
            qs_today = CustomerDailyMission.objects.select_for_update().filter(
                customer=customer, assign_date=today
            )
            try:
                entry = qs_today.get(owner_mission_id=mission_id)
            except CustomerDailyMission.DoesNotExist:
                return Response({"detail": "오늘 배정된 해당 미션이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

            # ✅ ASSIGNED 또는 ING만 완료 허용
            if entry.status not in [S.ASSIGNED, S.ING]:
                return Response({"detail": f"현재 상태가 '{entry.status}'라 완료 처리 불가합니다."},
                                status=status.HTTP_400_BAD_REQUEST)

            entry.status = S.COMPLETED
            entry.save(update_fields=["status"])

            # ✅ 남은 ASSIGNED/ING는 전부 무효
            qs_today.exclude(pk=entry.pk).filter(status__in=[S.ASSIGNED, S.ING]).update(status=S.INVALIDATED)

            data = CustomerDailyMissionSerializer(qs_today, many=True).data
            return Response({"date": str(today), "missions": data}, status=status.HTTP_200_OK)

