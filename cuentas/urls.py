from django.urls import path

from . import views

app_name = 'cuentas'

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_vista, name='login'),
    path('logout/', views.logout_vista, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
]
