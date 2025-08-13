from django.urls import path
from .views import CustomerView, CharacterView

urlpatterns = [
    path("", CustomerView.as_view()),          # /customer/  (GET, POST)
    path("<int:pk>/", CustomerView.as_view()), # /customer/1/ (GET, PUT, DELETE)

    path("character/", CharacterView.as_view()),             # /customer/character/  (GET, POST)
    path("character/<int:pk>/", CharacterView.as_view()),    # /customer/character/1/ (GET, PUT, DELETE)
]
