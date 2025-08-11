from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin", admin.site.urls),
    path("route", include("route.urls")),
    path("post", include("post.urls")),
    path("customer", include("customer.urls")),  # 최종: /customer/...
]
