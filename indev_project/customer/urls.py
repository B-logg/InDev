from django.contrib import admin
from django.urls import path
from .views import CustomerView

urlpatterns = [
    path('customer/', CustomerView.as_view()), # 전체 조회, 생성
    path('customer/<int:pk>/', CustomerView.as_view()), # 특정 조회, 수정, 삭제

]