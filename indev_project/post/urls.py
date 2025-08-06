from django.contrib import admin
from django.urls import path
from .views import PostMassilView

urlpatterns = [
    path('postmassil/', PostMassilView.as_view()),
    path('postmassil/<int:pk>/', PostMassilView.as_view()),
    
] 