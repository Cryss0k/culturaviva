from django.urls import path

from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('espectaculos/', views.lista, name='lista'),
    path('espectaculos/<slug:slug>/', views.detalle, name='detalle'),
    path('gestion/espectaculos/', views.gestion_lista, name='gestion_lista'),
    path('gestion/espectaculos/nuevo/', views.crear, name='crear'),
    path('gestion/espectaculos/<slug:slug>/editar/', views.editar, name='editar'),
    path('gestion/espectaculos/<slug:slug>/eliminar/', views.eliminar, name='eliminar'),
]
