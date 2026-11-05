"""Vistas de autenticación (Pablo: tareas P2, P3). Login, logout y perfil siguen como stubs."""
from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import RegistroForm


def _stub(nombre):
    return HttpResponse(f'Pendiente de implementar: {nombre} (Pablo)')


def registro(request):
    """Registra un cliente nuevo y lo deja con la sesión iniciada."""
    if request.user.is_authenticated:
        return redirect('portal:inicio')
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, f'¡Bienvenido/a, {usuario.username}! Tu cuenta fue creada.')
            return redirect('portal:inicio')
    else:
        form = RegistroForm()
    return render(request, 'cuentas/registro.html', {'form': form})


def login_vista(request):
    return _stub('cuentas:login')


def logout_vista(request):
    return _stub('cuentas:logout (POST)')


def perfil(request):
    return _stub('cuentas:perfil (login_required)')
