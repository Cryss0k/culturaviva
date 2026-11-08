"""Vistas de autenticación (Pablo: tareas P2, P3)."""
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render

from .forms import LoginForm, PerfilForm, RegistroForm


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


class LoginVista(LoginView):
    """Login con AuthenticationForm y mensaje de bienvenida."""

    def form_valid(self, form):
        messages.success(self.request, f'Hola de nuevo, {form.get_user().username}.')
        return super().form_valid(form)


login_vista = LoginVista.as_view(
    template_name='cuentas/login.html',
    authentication_form=LoginForm,
    redirect_authenticated_user=True,
)

# Django 5: LogoutView solo acepta POST (el navbar ya lo envía así).
logout_vista = LogoutView.as_view()


@login_required
def perfil(request):
    """Muestra los datos del usuario y permite editar el teléfono."""
    perfil_usuario = getattr(request.user, 'perfil', None)
    if perfil_usuario is None:  # p. ej. superusuario creado con createsuperuser
        messages.info(request, 'Tu cuenta no tiene un perfil asociado.')
        return redirect('portal:inicio')
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil_usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil fue actualizado.')
            return redirect('cuentas:perfil')
    else:
        form = PerfilForm(instance=perfil_usuario)
    return render(request, 'cuentas/perfil.html', {'form': form, 'perfil': perfil_usuario})
