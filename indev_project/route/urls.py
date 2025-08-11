from django.contrib import admin
from django.urls import path
from .views import RoutineView, VisitRoutineView

urlpatterns = [
    path('routine', RoutineView.as_view()), # 전체 조회, 생성
    path('routine/<int:pk>', RoutineView.as_view()), # 특정 조회, 수정, 삭제
    path('visitroutine', VisitRoutineView.as_view()), # 전체 조회, 생성
    path('visitroutine/<int:pk>', VisitRoutineView.as_view()), # 특정 조회, 수정, 삭제
    
]