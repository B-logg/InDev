# mission/urls.py
from django.urls import path
from .views import (
    OwnerMissionListCreateView, OwnerMissionDetailView,
    AssignMissionsView, CompleteMissionView
)

urlpatterns = [
    # OwnerMission CRUD
    path("owner-missions/", OwnerMissionListCreateView.as_view(), name="owner-mission-list-create"),
    path("owner-missions/<int:pk>/", OwnerMissionDetailView.as_view(), name="owner-mission-detail"),

    # 미션 배정(오늘자 조회/필요 시 생성)
    path("assign/<int:pk>/", AssignMissionsView.as_view(), name="assign-missions"),

    # 미션 완료 (오늘 배정된 특정 미션 완료)
    path("assign/<int:pk>/complete/<int:mission_id>/", CompleteMissionView.as_view(), name="complete-mission"),
]
