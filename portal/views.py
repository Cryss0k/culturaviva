"""Catálogo público y CRUD de gestión (Pablo: tareas P5 a P10). Por ahora son stubs,
excepto 'inicio' (renderiza base.html) y los manejadores de error 403/404."""
from django.http import HttpResponse
from django.shortcuts import render


def _stub(nombre):
    return HttpResponse(f'Pendiente de implementar: {nombre} (Pablo)')


def inicio(request):
    return render(request, 'portal/inicio.html')


def lista(request):
    return _stub('portal:lista')


def detalle(request, slug):
    return _stub(f'portal:detalle ({slug})')


def gestion_lista(request):
    return _stub('portal:gestion_lista (staff)')


def crear(request):
    return _stub('portal:crear (staff)')


def editar(request, slug):
    return _stub(f'portal:editar ({slug}) (staff)')


def eliminar(request, slug):
    return _stub(f'portal:eliminar ({slug}) (staff)')


def error_403(request, exception=None):
    return render(request, '403.html', status=403)


def error_404(request, exception=None):
    return render(request, '404.html', status=404)
