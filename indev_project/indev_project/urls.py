from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("route/", include("route.urls")),
    path("post/", include("post.urls")),
    path("customer/", include("customer.urls")),  # 최종: /customer/...
    path("mission/",include("missions.urls")),
    path("owner/",include("owner.urls")),
    path("category/",include("category.urls")),
    path("store/",include("store.urls")),
    path("flyers/",include("flyers.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
