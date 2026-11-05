"""Rutas raíz. Cada app define las suyas en su propio urls.py (con app_name)."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cuentas/', include('cuentas.urls')),
    path('reservas/', include('reservas.urls')),
    path('', include('portal.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'portal.views.error_403'
handler404 = 'portal.views.error_404'
