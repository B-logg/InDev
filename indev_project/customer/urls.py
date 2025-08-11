from django.urls import path
from .views import CustomerView

urlpatterns = [
    path("", CustomerView.as_view()),          # /customer/  (GET, POST)
    path("/<int:pk>", CustomerView.as_view()), # /customer/1/ (GET, PUT, DELETE)
]
