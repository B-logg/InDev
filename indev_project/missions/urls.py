# mission/urls.py
from django.urls import path
from .views import (
    ServiceMissionListCreateView, ServiceMissionDetailView,
    OwnerMissionListCreateView, OwnerMissionDetailView,
    AssignMissionsView
)

urlpatterns = [
    # ServiceMission CRUD
    path("service-missions/", ServiceMissionListCreateView.as_view(), name="service-mission-list-create"),
    path("service-missions/<int:pk>/", ServiceMissionDetailView.as_view(), name="service-mission-detail"),

    # OwnerMission CRUD
    path("owner-missions/", OwnerMissionListCreateView.as_view(), name="owner-mission-list-create"),
    path("owner-missions/<int:pk>/", OwnerMissionDetailView.as_view(), name="owner-mission-detail"),

    # 미션 배정
    path("customer/<int:pk>/", AssignMissionsView.as_view(), name="assign-missions"),
]
