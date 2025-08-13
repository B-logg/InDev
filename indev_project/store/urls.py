from django.contrib import admin
from django.urls import path
from .views import StoreView, AnalysisView

urlpatterns = [
    path("", StoreView.as_view()),             # /store/
    path("<int:pk>/", StoreView.as_view()),    # /store/1/

    path("analysis/", AnalysisView.as_view()),             # /store/analysis/
    path("analysis/<int:pk>/", AnalysisView.as_view()),    # /store/analysis/1/
] 