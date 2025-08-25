# mission/urls.py
from django.urls import path
from .views import (
    OwnerMissionListCreateView, OwnerMissionDetailView,
    AssignMissionsView, CompleteMissionView,OwnerMissionByStoreListView, StartMissionView
)

urlpatterns = [
    # OwnerMission CRUD
    path("owner-missions/", OwnerMissionListCreateView.as_view(), name="owner-mission-list-create"),
    path("owner-missions/<int:pk>/", OwnerMissionDetailView.as_view(), name="owner-mission-detail"),

    # ✅ 특정 가게의 미션 목록
    path("owner-missions/store/<int:store_id>/", OwnerMissionByStoreListView.as_view(),
         name="owner-mission-by-store"),

    # 미션 배정(오늘자 조회/필요 시 생성)
    path("assign/<int:pk>/", AssignMissionsView.as_view(), name="assign-missions"),
    path("assign/<int:pk>/start/<int:mission_id>/", StartMissionView.as_view(), name="start-mission"),

    # 미션 완료 (오늘 배정된 특정 미션 완료)
    path("assign/complete/<int:mission_id>/", CompleteMissionView.as_view(), name="complete-mission"),
]
