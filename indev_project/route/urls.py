from django.contrib import admin
from django.urls import path
from .views import RoutineView, VisitRoutineView

urlpatterns = [
    path('routine/', RoutineView.as_view()),
    path('routine/<int:pk>/', RoutineView.as_view()),
    path('visitroutine/', VisitRoutineView.as_view()),
    path('visitroutine/<int:pk>/', VisitRoutineView.as_view()),
    
]