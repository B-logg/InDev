from django.contrib import admin
from django.urls import path
from .views import PostMassilView

urlpatterns = [
    path('postmassil/', PostMassilView.as_view()), # 전체 조회, 생성
    path('postmassil/<int:pk>/', PostMassilView.as_view()), # 특정 조회, 수정, 삭제
    
] 