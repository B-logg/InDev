from django.contrib import admin
from django.urls import path
from .views import CategoryView

urlpatterns = [
    path("", CategoryView.as_view()),             # /category/
    path("<int:pk>/", CategoryView.as_view()),    # /category/1/
] 