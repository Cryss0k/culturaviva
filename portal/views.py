"""Catálogo público y CRUD de gestión (Pablo: tareas P5 a P10)."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from catalogo.models import Espectaculo, Genero
from cuentas.permisos import exige_staff

from .forms import EspectaculoForm

POR_PAGINA = 9
# Lista blanca: solo estos valores pueden llegar al order_by().
ORDENES = {
    'fecha_funcion': 'Fecha (próximas primero)',
    '-fecha_funcion': 'Fecha (lejanas primero)',
    'precio_entrada': 'Precio (menor a mayor)',
    '-precio_entrada': 'Precio (mayor a menor)',
    'titulo': 'Título (A-Z)',
    '-titulo': 'Título (Z-A)',
}


def inicio(request):
    """Portada con los próximos espectáculos disponibles."""
    proximos = Espectaculo.objects.disponibles().select_related('genero')[:6]
    generos = Genero.objects.filter(activo=True)
    return render(request, 'portal/inicio.html', {'proximos': proximos, 'generos': generos})


def lista(request):
    """Catálogo público con búsqueda, filtro por género, orden y paginación."""
    espectaculos = Espectaculo.objects.vigentes().select_related('genero')

    q = request.GET.get('q', '').strip()
    if q:
        espectaculos = espectaculos.filter(
            Q(titulo__icontains=q) | Q(codigo__icontains=q) | Q(descripcion__icontains=q))

    genero = request.GET.get('genero', '')
    if genero:
        espectaculos = espectaculos.filter(genero__slug=genero)

    orden = request.GET.get('orden', 'fecha_funcion')
    if orden not in ORDENES:
        orden = 'fecha_funcion'
    espectaculos = espectaculos.order_by(orden)

    pagina = Paginator(espectaculos, POR_PAGINA).get_page(request.GET.get('page'))
    params = request.GET.copy()
    params.pop('page', None)  # se conservan los filtros al cambiar de página
    return render(request, 'portal/lista.html', {
        'pagina': pagina,
        'generos': Genero.objects.filter(activo=True),
        'ordenes': ORDENES,
        'q': q, 'genero_actual': genero, 'orden_actual': orden,
        'querystring': params.urlencode(),
    })


def detalle(request, slug):
    """Detalle por slug; 404 si no existe o está dado de baja."""
    espectaculo = get_object_or_404(
        Espectaculo.objects.vigentes().select_related('genero'), slug=slug)
    return render(request, 'portal/detalle.html', {
        'espectaculo': espectaculo, 'cantidad_maxima': 6})


@login_required
@user_passes_test(exige_staff)
def gestion_lista(request):
    """Todos los espectáculos (activos e inactivos) para el personal."""
    espectaculos = Espectaculo.objects.select_related('genero').order_by('-activo', 'fecha_funcion')
    return render(request, 'portal/gestion_lista.html', {'espectaculos': espectaculos})


@login_required
@user_passes_test(exige_staff)
def crear(request):
    """C: crea un espectáculo (con imagen opcional en request.FILES)."""
    if request.method == 'POST':
        form = EspectaculoForm(request.POST, request.FILES)
        if form.is_valid():
            espectaculo = form.save()
            messages.success(request, f'«{espectaculo.titulo}» fue creado.')
            return redirect('portal:gestion_lista')
    else:
        form = EspectaculoForm()
    return render(request, 'portal/form_espectaculo.html', {'form': form, 'titulo': 'Nuevo espectáculo'})


@login_required
@user_passes_test(exige_staff)
def editar(request, slug):
    """U: edita un espectáculo con el formulario precargado."""
    espectaculo = get_object_or_404(Espectaculo, slug=slug)
    if request.method == 'POST':
        form = EspectaculoForm(request.POST, request.FILES, instance=espectaculo)
        if form.is_valid():
            form.save()
            messages.success(request, f'«{espectaculo.titulo}» fue actualizado.')
            return redirect('portal:gestion_lista')
    else:
        form = EspectaculoForm(instance=espectaculo)
    return render(request, 'portal/form_espectaculo.html', {
        'form': form, 'titulo': f'Editar: {espectaculo.titulo}', 'espectaculo': espectaculo})


@login_required
@user_passes_test(exige_staff)
def eliminar(request, slug):
    """D: confirmación previa y baja lógica (activo=False). No borra el registro."""
    espectaculo = get_object_or_404(Espectaculo, slug=slug)
    if request.method == 'POST':
        espectaculo.activo = False
        espectaculo.save(update_fields=['activo', 'actualizado'])
        messages.success(request, f'«{espectaculo.titulo}» fue dado de baja.')
        return redirect('portal:gestion_lista')
    return render(request, 'portal/confirmar_eliminar.html', {'espectaculo': espectaculo})


def error_403(request, exception=None):
    return render(request, '403.html', status=403)


def error_404(request, exception=None):
    return render(request, '404.html', status=404)
