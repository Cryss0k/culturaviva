"""QuerySet personalizado de Espectaculo (contrato con Pablo y con reservas)."""
from django.db import models
from django.utils import timezone


class EspectaculoQuerySet(models.QuerySet):
    def con_genero(self):
        """Evita el problema N+1 al mostrar el género de cada espectáculo."""
        return self.select_related('genero')

    def del_genero(self, slug):
        """Filtra por el slug del género (para el filtro del catálogo)."""
        return self.filter(genero__slug=slug)

    def vigentes(self):
        """Registros sin baja lógica (activo=True)."""
        return self.filter(activo=True)

    def disponibles(self):
        """Vigentes, en estado 'disponible', con cupos y con fecha futura."""
        return self.vigentes().filter(
            estado='disponible',
            entradas_disponibles__gt=0,
            fecha_funcion__gte=timezone.now(),
        )
