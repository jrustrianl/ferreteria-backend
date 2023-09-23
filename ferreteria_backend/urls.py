from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView

from rest_framework import routers
from ferreteria import views

router = routers.DefaultRouter()
router.register(r'cliente', views.ClienteViewSet, basename='Cliente')
router.register(r'login', views.LoginViewSet, basename='Login')
router.register(r'home', views.HomeViewSet, basename='Home')
router.register(r'categoria', views.CategoriaViewSet, basename='Categoria')
router.register(r'marca', views.MarcaViewSet, basename='Marca')
router.register(r'producto', views.ProductoViewSet, basename='Producto')

urlpatterns = [
    #path("ferreteria/", include("ferreteria.urls")),
    path('api-auth/', include(router.urls)),
    path("admin/", admin.site.urls),
    re_path(r'^$', RedirectView.as_view(url='/admin'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
