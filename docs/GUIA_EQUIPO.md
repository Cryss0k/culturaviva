# Guía del equipo (Cristian y Pablo)

## 1. Reparto
| App | Dueño | Contenido |
|---|---|---|
| `catalogo` | Cristian | modelos, admin, validators, managers, `poblar_datos`, fixtures, tests |
| `reservas` | Cristian | carrito en sesión, vistas, context processor, comprobante |
| `cuentas` | Pablo | registro, login, logout, Perfil, permisos |
| `portal` | Pablo | home, catálogo público, detalle, CRUD de gestión, `templates/base.html`, estáticos |

Archivos compartidos (`config/settings.py`, `config/urls.py`): solo PR pequeños y aviso. `templates/base.html` es de Pablo; Cristian lo extiende y pide cambios por issue.

Cada integrante documenta su bitácora de IA (mínimo 3 casos propios) en su sección del README.

## 2. Normas de nomenclatura
- Dominio en español sin tildes ni ñ (`espectaculo`, `precio_entrada`); lo propio de Django en inglés.
- Variables y funciones `snake_case`; clases `PascalCase` en singular; constantes `MAYUSCULAS_CON_GUION_BAJO`.
- Formularios `<Modelo>Form`; vistas verbo + sustantivo; URLs con namespace (`portal:detalle`).
- Plantillas en `templates/<app>/nombre.html`; clases CSS propias `cv-nombre`.
- Ramas `tipo/parte-descripcion` (ej: `feature/pablo-crud-crear`).
- PEP 8, líneas de máximo 100 caracteres, imports ordenados (estándar, terceros, locales), docstrings en español.
- Dinero con `Decimal`. `select_related('genero')` al mostrar el género. Todo POST con `{% csrf_token %}`.
- Vistas finas: la lógica va en modelos, managers, `carrito.py` o formularios. Mensajes con `django.contrib.messages`.
- Nunca confiar en precios del cliente: se recalculan desde la BD.

## 3. Contratos
**Modelos** (ver `catalogo/models.py` y `cuentas/models.py`): `Genero`, `Espectaculo` (FK con PROTECT, MinValueValidator, choices, ImageField, baja lógica `activo`) y `Perfil`.
`Espectaculo.objects.vigentes()` y `.disponibles()` ya existen.

**URLs** (nombres fijos, ver `config/tests.py`): `portal:{inicio,lista,detalle,gestion_lista,crear,editar,eliminar}`,
`cuentas:{registro,login,logout,perfil}`, `reservas:{ver,agregar,modificar,eliminar,vaciar,confirmar,comprobante}`.

**base.html**: bloques `title`, `content`, `extra_css`, `extra_js`; el navbar muestra `{{ carrito_total_items }}`.

**Carrito**: ver docstring de `reservas/carrito.py` (estructura en sesión, interfaz y fórmula con recargo 10% e IVA 19%).

## 4. Tareas
**Cristian:** C1 entorno · C2 modelos · C3 validators/QuerySet · C4 `poblar_datos` · C5 admin corporativo · C6 ModelAdmin avanzado · C7 clase Carrito · C8 vistas de reservas · C9 context processor · C10 tests · C11 docs e IA.

**Pablo:** P1 base.html/UI · P2 registro y perfil · P3 login/logout · P4 permisos · P5 catálogo público (Q, filtro, orden, Paginator) · P6 detalle · P7 crear · P8 editar · P9 eliminar · P10 gestión · P11 tests · P12 docs e IA.

## 5. Flujo en GitHub
1. `git switch main && git pull`
2. `git switch -c feature/pablo-crud-crear`
3. Commits pequeños y frecuentes, formato `tipo(app): descripción` (`feat`, `fix`, `docs`, `test`, `refactor`, `chore`).
4. `git pull --rebase origin main`, `git push -u origin <rama>` y abrir PR con `Closes #N`.
5. El compañero revisa y aprueba. Merge con **merge commit o rebase** (no squash) para conservar los commits de cada autor.
6. Configurar `git config user.name` y `user.email` con el correo de la cuenta de GitHub.

## 6. Definition of Done
Cumple normas, migraciones incluidas, al menos un test feliz y uno de error, sin secretos, CSRF en POST y PR revisado.
