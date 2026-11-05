from django.urls import path

from . import views

app_name = 'reservas'

urlpatterns = [
    path('carrito/', views.ver, name='ver'),
    path('agregar/<int:espectaculo_id>/', views.agregar, name='agregar'),
    path('modificar/<int:espectaculo_id>/', views.modificar, name='modificar'),
    path('eliminar/<int:espectaculo_id>/', views.eliminar, name='eliminar'),
    path('vaciar/', views.vaciar, name='vaciar'),
    path('confirmar/', views.confirmar, name='confirmar'),
    path('comprobante/', views.comprobante, name='comprobante'),
]
