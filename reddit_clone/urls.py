from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),             # Admin panel
    path("reddit/", include("reddit.urls")),     # Main app URLs
]
