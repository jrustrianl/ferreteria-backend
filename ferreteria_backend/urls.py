from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("ferreteria/", include("ferreteria.urls")),
    path("admin/", admin.site.urls),
]
