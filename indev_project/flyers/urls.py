from django.urls import path
from .views import GenerateFlyerView

urlpatterns = [
    path("generate/", GenerateFlyerView.as_view(), name="generate-flyer"),
]
