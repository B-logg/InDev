from django.contrib import admin
from django.urls import path
from .views import OwnerView

urlpatterns = [
    path("", OwnerView.as_view()),             # /owner/
    path("<int:pk>/", OwnerView.as_view()),    # /owner/1/
] 