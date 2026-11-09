# CulturaViva Producciones

Plataforma web para explorar espectáculos culturales (teatro, música, danza, stand-up y cine) y reservar entradas en línea, desarrollada con **Django**.

Evaluación Sumativa N° 3 · Programación Back End (T13041) · Unidad 2: Framework Back End
Proyecto de libre elección: *Productora de Eventos y Cultura*


---

## Índice

1. [Ficha de registro de la propuesta](#1-ficha-de-registro-de-la-propuesta)
2. [Funcionalidades](#2-funcionalidades)
3. [Instalación paso a paso](#3-instalación-paso-a-paso)
4. [Credenciales de prueba](#4-credenciales-de-prueba)
5. [Estructura del proyecto](#5-estructura-del-proyecto)
6. [Modelo de datos](#6-modelo-de-datos)
7. [Rutas y roles](#7-rutas-y-roles)
8. [Documentación técnica: parte de Cristian](#8-documentación-técnica-parte-de-cristian)
9. [Documentación técnica: parte de Pablo](#9-documentación-técnica-parte-de-pablo)
10. [Pruebas automáticas](#10-pruebas-automáticas)
11. [Bitácora de prompts de Inteligencia Artificial](#11-bitácora-de-prompts-de-inteligencia-artificial)
12. [Trabajo colaborativo en Git y GitHub](#12-trabajo-colaborativo-en-git-y-github)

---

## 1. Ficha de registro de la propuesta

| Campo | Valor |
|---|---|
| Nombre de la organización o plataforma | CulturaViva Producciones |
| Modelo de negocio / giro | Productora de eventos y espectáculos culturales con venta de entradas en línea |
| Integrantes del equipo | Cristian Molina — RUT 22.327.826-4 · Pablo Pizarro — RUT 22.057.608-6 |
| Entidad de contexto / agrupación (ORM) | `Genero` (Teatro, Música, Danza, Stand-up, Cine) |
| Entidad principal gestionable (ORM) | `Espectaculo` (función con sala, aforo, valor y fecha) |
| Propósito de la sesión (`request.session`) | Carrito de entradas con reserva temporal, cargo por servicio (10%) e IVA (19%) |
| Repositorio | https://github.com/Cryss0k/culturaviva |

---

## 2. Funcionalidades

- **Catálogo público** de espectáculos con tarjetas, buscador por texto, filtro por género, ordenamiento y paginación.
- **Carrito de entradas en sesión**: agregar, cambiar cantidad, quitar y vaciar, con validación de cupos y desglose de subtotal, cargo por servicio, IVA y total. El contador aparece en el navbar de todas las páginas.
- **Comprobante simulado** al confirmar la solicitud (requiere iniciar sesión). No se guarda en la base de datos ni descuenta stock.
- **Registro, inicio y cierre de sesión** con perfil de usuario (RUT, teléfono y rol institucional).
- **Panel de gestión protegido** para el personal: crear, editar y dar de baja espectáculos, con imágenes.
- **Django Admin personalizado** con la identidad de la plataforma.

**Tecnologías:** Python 3.12 a 3.14 · Django 5.2 · Pillow · python-dotenv · Bootstrap 5.3 · SQLite

---

## 3. Instalación paso a paso

### Requisitos previos
- **Python 3.12, 3.13 o 3.14** (comprobar con `python --version`)
- **Git**

### Paso 1: Clonar el repositorio
```bash
git clone https://github.com/Cryss0k/culturaviva.git
cd culturaviva
```

### Paso 2: Crear y activar el entorno virtual
**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```
Si PowerShell bloquea el script, ejecuta primero `Set-ExecutionPolicy -Scope Process Bypass`.

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```
Cuando el entorno está activo, el prompt muestra `(.venv)` al inicio.

### Paso 3: Instalar las dependencias
```bash
pip install -r requirements.txt
```
Instala Django 5.2.8, Pillow 12.0.0 y python-dotenv 1.0.1 (versiones compatibles con Python 3.12 a 3.14).

### Paso 4: Configurar las variables de entorno
Copia la plantilla y edítala:

**Windows:** `copy .env.example .env`
**Linux / macOS:** `cp .env.example .env`

Variables disponibles en `.env`:

| Variable | Descripción | Valor para desarrollo |
|---|---|---|
| `SECRET_KEY` | Clave secreta de Django (usa una larga y aleatoria) | cualquier texto largo |
| `DEBUG` | Modo desarrollo | `True` |
| `ALLOWED_HOSTS` | Hosts permitidos, separados por coma | `127.0.0.1,localhost` |
| `DB_NAME` | Archivo de la base de datos SQLite | `db.sqlite3` |

Para generar una `SECRET_KEY` nueva:
```bash
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
```
El archivo `.env` está en `.gitignore` y **no se sube** al repositorio. Lo que se sube es `.env.example`.

### Paso 5: Crear la base de datos
```bash
python manage.py migrate
```
Crea el archivo `db.sqlite3` con todas las tablas. **Este paso es obligatorio y debe hacerse antes del Paso 6**; si se omite, `poblar_datos` falla con `no such table`. Para comprobarlo:
```bash
python manage.py showmigrations
```
Todas las migraciones deben aparecer marcadas con `[X]`.

### Paso 6: Cargar la base de datos de prueba
```bash
python manage.py poblar_datos
```
Crea 5 géneros, 10 espectáculos con imágenes de portada y los dos usuarios de prueba (ver sección 4). Se puede ejecutar varias veces sin duplicar datos. Opciones:
- `--limpiar`: borra espectáculos, géneros y usuarios de prueba antes de cargar.
- `--sin-imagenes`: no genera imágenes de portada.

Al terminar, el comando muestra por consola los usuarios y contraseñas creados.

### Paso 7: Iniciar el servidor
```bash
python manage.py runserver
```
Abre <http://127.0.0.1:8000/> en el navegador. El panel de administración está en <http://127.0.0.1:8000/admin/>.

### Paso 8 (opcional): Ejecutar las pruebas
```bash
python manage.py test
```
Las pruebas usan su propia base de datos temporal; no modifican `db.sqlite3`.

### Reiniciar la base de datos de prueba
Si los datos quedaron desordenados o se quiere partir desde cero, hay dos opciones:

**Opción 1: recargar solo los datos de demostración**
```bash
python manage.py poblar_datos --limpiar
```

**Opción 2: recrear la base completa**

*Windows (PowerShell):*
```powershell
Remove-Item db.sqlite3
python manage.py migrate
python manage.py poblar_datos
```
*Linux / macOS:*
```bash
rm db.sqlite3
python manage.py migrate
python manage.py poblar_datos
```
`db.sqlite3` es un archivo local que no está en el repositorio (está en `.gitignore`), por lo que borrarlo no afecta al código. Si se usa el panel de gestión para subir imágenes, quedan en la carpeta `media/`, que tampoco se sube a GitHub.

### Solución de problemas frecuentes

| Síntoma | Solución |
|---|---|
| `ModuleNotFoundError: No module named 'django'` | El entorno virtual no está activo o faltó el Paso 3 |
| `no such table: catalogo_genero` (u otra tabla) al ejecutar `poblar_datos` o abrir el sitio | Faltan aplicar las migraciones: ejecutar `python manage.py migrate` **antes** de `poblar_datos` |
| `migrate` no muestra migraciones de `catalogo` o `cuentas` | Las migraciones no están en el repositorio: ejecutar `python manage.py makemigrations catalogo cuentas`, volver a correr `migrate` y subir las carpetas `migrations/` a GitHub |
| `Failed building wheel for pillow` / `RequiredDependencyException: zlib` | El `requirements.txt` está desactualizado respecto de la versión de Python (por ejemplo, Pillow 11 con Python 3.14). Hacer `git pull` y volver a ejecutar `pip install -r requirements.txt` |
| `poblar_datos` falla al crear los usuarios con un error de RUT | El validador de RUT de `cuentas` rechaza el RUT de prueba. Revisar `USUARIOS` en `catalogo/management/commands/poblar_datos.py` |
| La base de datos quedó con datos incorrectos | Ver "Reiniciar la base de datos de prueba" |
| No se ven las imágenes | Verifica que `DEBUG=True` en `.env` |
| `Your models have changes that are not yet reflected` | Ejecutar `python manage.py makemigrations`, luego `migrate`, y subir la migración nueva |

La guía ampliada está en [`docs/ENTORNO.md`](docs/ENTORNO.md).

---

## 4. Credenciales de prueba

Se crean con `python manage.py poblar_datos` (después de `migrate`):

| Rol | Usuario | Contraseña | Permisos |
|---|---|---|---|
| Administrador (staff y superusuario) | `admin` | `Admin12345!` | Django Admin, panel de gestión y compra |
| Cliente (usuario estándar) | `cliente` | `Cliente12345!` | Catálogo, carrito y comprobante |

Son credenciales de demostración; no deben usarse en un entorno real.

---

## 5. Estructura del proyecto

```
culturaviva/
├── config/        Configuración del proyecto (settings, urls)
├── catalogo/      [Cristian] Modelos, admin, validadores, comando poblar_datos
├── reservas/      [Cristian] Carrito en sesión, comprobante, context processor
├── cuentas/       [Pablo] Registro, login, logout, perfil y permisos
├── portal/        [Pablo] Catálogo público, detalle y CRUD de gestión
├── templates/     base.html y páginas de error 403 y 404
├── static/        Archivos estáticos globales
├── fixtures/      Datos mínimos de ejemplo
├── docs/          Guías del equipo y del entorno
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## 6. Modelo de datos

```
Genero 1 ──────< Espectaculo      (ForeignKey, on_delete=PROTECT)
User   1 ────── 1 Perfil          (OneToOneField)
```

**Genero** (entidad de contexto): `nombre` (único), `slug`, `descripcion`, `icono`, `activo`.

**Espectaculo** (entidad principal):

| Campo | Detalle |
|---|---|
| `genero` | ForeignKey a Genero con `PROTECT` (no se puede borrar un género con espectáculos) |
| `codigo` | Único, formato `XXX-000` (ej. `TEA-001`) |
| `slug` | Único, para las URLs amigables |
| `titulo`, `descripcion`, `elenco`, `sala` | Datos descriptivos |
| `fecha_funcion`, `duracion_minutos` | Datos de la función |
| `aforo`, `entradas_disponibles` | Cupos, con `MinValueValidator` |
| `precio_entrada` | Valor en CLP, con `MinValueValidator(0)` |
| `estado` | `choices`: disponible, agotado, suspendido, finalizado |
| `imagen` | `ImageField` (carpeta `media/espectaculos/`) |
| `activo` | Baja lógica: desactiva sin borrar físicamente |
| `creado`, `actualizado` | Auditoría automática |

Regla adicional en `clean()`: las entradas disponibles no pueden superar el aforo.

**Perfil**: `usuario` (OneToOne), `rut` (único), `telefono` y `rol_institucional` (cliente, boletería o productor).

QuerySet de `Espectaculo`: `vigentes()`, `disponibles()`, `con_genero()` y `del_genero(slug)`.

---

## 7. Rutas y roles

| Nombre de la ruta | URL | Acceso |
|---|---|---|
| `portal:inicio` | `/` | Público |
| `portal:lista` | `/espectaculos/` | Público |
| `portal:detalle` | `/espectaculos/<slug>/` | Público |
| `portal:gestion_lista` | `/gestion/espectaculos/` | Staff |
| `portal:crear` | `/gestion/espectaculos/nuevo/` | Staff |
| `portal:editar` | `/gestion/espectaculos/<slug>/editar/` | Staff |
| `portal:eliminar` | `/gestion/espectaculos/<slug>/eliminar/` | Staff |
| `cuentas:registro` | `/cuentas/registro/` | Anónimo |
| `cuentas:login` | `/cuentas/login/` | Anónimo |
| `cuentas:logout` | `/cuentas/logout/` (POST) | Autenticado |
| `cuentas:perfil` | `/cuentas/perfil/` | Autenticado |
| `reservas:ver` | `/reservas/carrito/` | Público |
| `reservas:agregar` / `modificar` / `eliminar` / `vaciar` | `/reservas/...` (POST) | Público |
| `reservas:confirmar` | `/reservas/confirmar/` (POST) | Autenticado |
| `reservas:comprobante` | `/reservas/comprobante/` | Autenticado |
| Django Admin | `/admin/` | Staff |

---

## 8. Documentación técnica: parte de Cristian

*Responsable de: capa de datos, Django Admin, comando de carga y carrito en sesión.*

### Capa de datos y migraciones
Los modelos `Genero` y `Espectaculo` están en `catalogo/models.py`. Usan validadores numéricos, estados cerrados con `choices`, soporte de imágenes con `ImageField` y baja lógica con `activo`. El campo `codigo` se valida con la expresión regular `^[A-Z]{3}-\d{3}$` (`catalogo/validators.py`). Las migraciones están versionadas en cada app.

### Comando `poblar_datos`
Ubicado en `catalogo/management/commands/poblar_datos.py`. Es idempotente (usa `update_or_create` por código), genera fechas relativas a hoy, deja un espectáculo agotado, uno suspendido y uno finalizado para probar los estados, y crea imágenes de portada con Pillow.

### Django Admin
Configurado en `catalogo/admin.py`:
- Títulos corporativos: `site_header`, `site_title` e `index_title`.
- `EspectaculoAdmin`: `list_display`, `list_filter` (género, estado, vigencia), `search_fields` (código, título, elenco, sala, descripción), `list_editable` (valor, estado y vigencia), `fieldsets` por secciones, `date_hierarchy`, vista previa de imagen y acciones masivas para activar y desactivar.
- `list_select_related` y `annotate(Count)` evitan consultas N+1.

### Carrito de entradas (`request.session`)
Implementado en `reservas/carrito.py`:
- En la sesión se guarda solo `{id_espectaculo: {cantidad}}`. Los precios y cupos se leen de la base de datos en cada cálculo, de modo que el cliente no puede manipularlos.
- **Validaciones** al agregar o modificar: espectáculo vigente y disponible, función futura, máximo 6 entradas por función y cupos suficientes.
- **Operaciones:** agregar (acumula), modificar cantidad (0 elimina), eliminar un ítem y vaciar.
- **Desglose:** `subtotal`, cargo por servicio (10%), IVA (19% sobre subtotal más cargo) y `total`, redondeados a pesos enteros con `Decimal`.
- **Context processor** `carrito_contador`: inyecta `carrito_total_items` en el navbar de todas las páginas sin consultar la base de datos.
- **Confirmación** (`@login_required` y POST): valida el carrito, genera un comprobante simulado con código `CV-AAAAMMDD-XXXXXX`, lo guarda en la sesión, vacía el carrito y redirige al comprobante.
- **Seguridad:** todas las acciones que modifican estado son POST con `{% csrf_token %}`. El parámetro `next` se valida con `url_has_allowed_host_and_scheme` para evitar redirecciones abiertas.

Los porcentajes y el máximo por compra se configuran en `config/settings.py` (`RECARGO_SERVICIO_PORCENTAJE`, `IVA_PORCENTAJE`, `MAX_ENTRADAS_POR_COMPRA`).

---

## 9. Documentación técnica: parte de Pablo

*Responsable de: autenticación, seguridad, catálogo público, CRUD de gestión e interfaz.*

### Autenticación y perfil
- **Registro** (`cuentas:registro`): formulario con usuario, correo, contraseña, RUT (validado con el algoritmo módulo 11 en `cuentas/validators.py`) y teléfono. El RUT se guarda normalizado (`12345678-5`) y es único. Crea el `User` y su `Perfil` en una misma transacción (`transaction.atomic`) e inicia la sesión al terminar.
- **Inicio de sesión** con `AuthenticationForm` (estilos Bootstrap) y **cierre de sesión por POST** con CSRF.
- **Perfil** (`cuentas:perfil`): requiere sesión; muestra usuario, correo, RUT y rol, y permite editar solo el teléfono. Una cuenta sin `Perfil` (por ejemplo, un superusuario creado con `createsuperuser`) es redirigida con un mensaje.

### Control de acceso por roles
- Las rutas de gestión usan `@login_required` y `@user_passes_test(exige_staff)` (`cuentas/permisos.py`).
- `exige_staff` lanza `PermissionDenied`: un usuario anónimo es redirigido al login y un usuario autenticado sin permisos recibe la página **403**. Con `es_staff` a secas, un cliente con sesión sería redirigido al login en lugar de recibir el 403.
- Todos los formularios POST incluyen `{% csrf_token %}`.

### Catálogo público (Read)
- Tarjetas Bootstrap con imagen (o marcador si no tiene), género, fecha, valor y estado.
- **Buscador** multi-campo con objeto `Q` (título, código y descripción).
- **Filtro** por género, **ordenamiento** (fecha, valor, título) con lista blanca de campos permitidos (`ORDENES`) y **paginación** con `Paginator` (9 por página) que conserva los filtros en la URL.
- **Detalle** accesible por `slug` (404 si no existe o está dado de baja), con formulario para agregar entradas al carrito solo si el espectáculo se puede reservar.
- Las consultas usan `vigentes()` y `select_related('genero')`.

### Gestión de espectáculos (Create, Update, Delete)
- **Crear:** `ModelForm` con estilos Bootstrap 5, `enctype="multipart/form-data"` y procesamiento de `request.FILES`. Validaciones `clean_codigo` (mayúsculas y único), `clean_precio_entrada` (no negativo) y `clean_entradas_disponibles` (no mayor al aforo). El `slug` se genera automáticamente a partir del título y se mantiene único.
- **Editar:** formulario precargado con la instancia; la validación de unicidad excluye el propio registro y el `slug` no cambia.
- **Eliminar:** pantalla de confirmación previa y **baja lógica** (`activo=False`); el registro no se borra y puede reactivarse desde «Editar». Los géneros se administran desde el Django Admin, donde `on_delete=PROTECT` impide borrar un género que tenga espectáculos asociados.
- **Listado de gestión** solo para staff, con registros activos e inactivos.

### Interfaz de usuario
Plantilla maestra `templates/base.html` con navbar responsivo (muestra el contador del carrito y enlaces según el rol), mensajes del sistema con el *messages framework*, pie de página y páginas 403 y 404. Se agregaron los componentes reutilizables `templates/includes/campos_form.html` (renderiza los formularios con errores por campo) y `templates/includes/card_espectaculo.html`. Diseño responsivo con Bootstrap 5.

---

## 10. Pruebas automáticas

```bash
python manage.py test
```

| Módulo | Qué se prueba |
|---|---|
| `catalogo/tests` | Validadores, `choices`, `PROTECT`, `clean()` del aforo, QuerySet, comando `poblar_datos` y Django Admin |
| `reservas/tests` | Carrito (límites, cupos, estados, fórmula con redondeo), vistas, contador global y comprobante |
| `cuentas/tests` | Validación de RUT (módulo 11), registro (crea `User` y `Perfil`), login, logout solo por POST, perfil y helpers de permisos |
| `portal/tests` | Catálogo (búsqueda con `Q`, filtro, orden con lista blanca, paginación), detalle, permisos de gestión (anónimo 302, cliente 403, staff 200), crear, editar, baja lógica y flujo completo |
| `config/tests.py` | Existencia de todas las rutas con nombre |

---

## 11. Bitácora de prompts de Inteligencia Artificial

Se utilizó IA como apoyo en arquitectura ORM, optimización de consultas y seguridad, evaluando críticamente cada respuesta antes de adaptarla. Cada integrante puede explicar el código resultante y justificar sus decisiones.

### Bitácora de Cristian

Herramienta utilizada en los tres casos: **Claude** (Anthropic). Los prompts se transcriben con la ortografía corregida; el contenido es el original.

#### Caso 1: Arquitectura del proyecto y configuración del entorno
- **Área:** Arquitectura ORM y entorno
- **Prompt utilizado:**
  > necesito que me ayudes a preparar un documento con todos los índices y el plan de desarrollo muy detalladamente (normas de variables, etc.), esto que incluyo todo lo necesario para que un equipo desarrolle el siguiente software con Django con el objetivo de cumplir los siguientes requerimientos de evaluación (el mío es de Productora de Eventos y Cultura). Divide todo el trabajo en 2 partes iguales independientes, es decir, que puedan avanzar sin que el otro haya terminado. Todo esto enfocado a GitHub. Divide todo en Cristian y Pablo; yo subiré la base del proyecto y de ahí ya empezaremos a trabajar en GitHub los dos. Aquí está el documento.

  *(Se adjuntó el documento de la evaluación sumativa N° 3.)*
- **Respuesta técnica (resumen):** Un plan de desarrollo con la división del trabajo en cuatro apps (`catalogo`, `reservas`, `cuentas`, `portal`), los modelos `Genero` y `Espectaculo` con `ForeignKey(on_delete=PROTECT)`, `MinValueValidator`, `choices` para el estado, `ImageField` y baja lógica con `activo`, un contrato de URLs entre ambos integrantes y una base de proyecto con `requirements.txt` de versiones fijas.
- **Evaluación crítica:**
  1. El modelo propuesto no impedía que `entradas_disponibles` fuera mayor que el `aforo`, una inconsistencia posible desde el admin o desde un formulario.
  2. Las versiones fijadas inicialmente (Django 5.1.4 y Pillow 11.0.0) fallaron al instalar el proyecto en un clon limpio con Python 3.14 en Windows: Pillow no tenía binarios para esa versión y el error terminaba en `RequiredDependencyException: zlib`. Esto solo se detectó al probar la instalación real; no bastaba con confiar en la respuesta de la IA.
- **Adaptación aplicada:**
  1. Se agregó `Espectaculo.clean()` en `catalogo/models.py` para validar la regla del aforo.
  2. Se actualizó `requirements.txt` a Django 5.2.8 y Pillow 12.0.0, versiones con soporte oficial de Python 3.14 según su documentación, y se ajustó el README (versiones de Python y solución de problemas).
- **Evidencia:** [Pull Request #1](https://github.com/Cryss0k/culturaviva/pull/1); commits [`002e566`](https://github.com/Cryss0k/culturaviva/commit/002e56607b1c375e9b519fb5d7ff160bdb8c16ea) (validación del aforo y guía de entorno) y [`9116f64`](https://github.com/Cryss0k/culturaviva/commit/9116f648690f01df36d028d55d761fe28b03db31) (actualización de Django y Pillow)

#### Caso 2: Seguridad y diseño del carrito en sesión, y optimización de consultas
- **Área:** Seguridad, sesiones y optimización de consultas
- **Prompt utilizado:**
  > ¿Podrías ayudarme a completar mi parte, la de Cristian? Aplicándolo por parches al repo de GitHub, así tengo un mayor control, en vez de subir todo de una.
- **Respuesta técnica (resumen):** Una serie de parches, uno por tarea, con el comando `poblar_datos`, la configuración del Django Admin, la clase `Carrito` que guarda en `request.session` solo el id y la cantidad, las vistas y plantillas del carrito y del comprobante, el context processor del contador y pruebas automáticas. Incluyó `select_related`, `in_bulk` y `annotate(Count)` para evitar consultas N+1.
- **Evaluación crítica:**
  1. Guardar solo id y cantidad evita que el cliente manipule precios y mantiene la sesión serializable en JSON (un `Decimal` no lo es). Precios y cupos se recalculan siempre desde la base de datos.
  2. Se revisó que el carrito use `session.get()` y no `setdefault()`, para no crear una sesión por cada visitante que solo navega.
  3. La confirmación genera un comprobante simulado sin descontar stock, de acuerdo con la rúbrica (colección transitoria sin persistencia inmediata).
  4. La IA advirtió que no pudo ejecutar el código ni las pruebas en su entorno, por lo que la verificación se hizo localmente con `python manage.py test` y `poblar_datos`.
- **Adaptación aplicada:** `reservas/carrito.py` con validación de estado, fecha futura, máximo por compra y cupos; `reservas/views.py` con `@require_POST`, `@login_required` en la confirmación y `url_has_allowed_host_and_scheme` contra redirecciones abiertas; `EspectaculoQuerySet.con_genero()`, `list_select_related` en el admin y `Carrito.items()` con una sola consulta, comprobado con `assertNumQueries`.
- **Evidencia:** [Pull Request #1](https://github.com/Cryss0k/culturaviva/pull/1); commits [`abade5e`](https://github.com/Cryss0k/culturaviva/commit/abade5efedada36495b51a9007c2935519d59f58) (clase `Carrito` en sesión), [`5f8c031`](https://github.com/Cryss0k/culturaviva/commit/5f8c0319e366cb53aba4c6da17d509f1623617be) (vistas, plantillas y contador) y [`4828a26`](https://github.com/Cryss0k/culturaviva/commit/4828a26b217480eb01f76ed9adee0a16d52f51e3) (pruebas)

#### Caso 3: Migraciones y conflictos de integración
- **Área:** ORM y migraciones
- **Prompt utilizado:**
  > Aquí estoy teniendo un conflicto

  *(Se pegó el contenido de `cuentas/migrations/0001_initial.py` con las marcas de conflicto `<<<<<<< feature/pablo-parte-b` y `>>>>>>> main`.)*
  Consulta de seguimiento, tras clonar el proyecto y ejecutar `poblar_datos`:
  > pasa esto al ejecutar poblar datos

  *(Se pegó el error `sqlite3.OperationalError: no such table: catalogo_genero`.)*
- **Respuesta técnica (resumen):** Para el conflicto, conservar la versión de la rama de Pablo, porque su modelo `Perfil` ya usa `validators=[validar_rut]` y la migración debe reflejar el estado final del modelo; luego cerrar el merge con `git add` y `git commit` y comprobar con `makemigrations --check`. Para el error, explicó que faltaba aplicar las migraciones antes de cargar los datos.
- **Evaluación crítica:**
  1. Una migración en conflicto no se resuelve eligiendo un lado al azar: debe coincidir con los modelos finales, y esa coincidencia se verifica con `makemigrations --check`.
  2. La IA detectó que la migración de `main` se había generado con otra versión de Django (6.1.1) que la fijada en `requirements.txt`, lo que obliga a que ambos integrantes usen las mismas versiones.
  3. El error `no such table` se debía al orden de los comandos, no a un fallo del código.
- **Adaptación aplicada:** Se resolvió `cuentas/migrations/0001_initial.py` con el `validar_rut`, se alineó el entorno con `requirements.txt` y se documentó en el README que `migrate` debe ejecutarse antes de `poblar_datos`, junto con el procedimiento para reiniciar la base de datos de prueba.
- **Evidencia:** [Pull Request #2](https://github.com/Cryss0k/culturaviva/pull/2); commits [`75b6629`](https://github.com/Cryss0k/culturaviva/commit/75b6629c23002c26324675ab6eec7159344229ec) (migraciones iniciales de `Perfil`) y [`c093bb4`](https://github.com/Cryss0k/culturaviva/commit/c093bb4124d65936f3f2e5130b6adb6c8b051b99) (merge de `main` con resolución del conflicto)

### Bitácora de Pablo

Herramienta utilizada en todos los casos: **Claude** (Anthropic). Los prompts se transcriben con la ortografía corregida; el contenido es el original. La guía por pasos y el código de la parte B fueron generados por Claude a partir del plan de desarrollo y del repositorio; Pablo los copió al proyecto, los ejecutó localmente con `python manage.py test` y resolvió los problemas de integración del Caso 4.

#### Caso 1: Seguridad de rutas y roles
- **Área:** Seguridad
- **Prompt utilizado:**
  > Necesito hacer mi parte (Pablo), ayúdame con un paso a paso para terminarlo hoy.

  *(Se adjuntó el plan de desarrollo de la plataforma de productora de eventos.)*
  *Contexto técnico:* el plan exige proteger las rutas de gestión por rol, distinguir al usuario anónimo del cliente sin permisos (redirección al login frente a respuesta 403), proteger los formularios contra CSRF y cerrar sesión solo por POST. El prompt es general; la solicitud técnica concreta se desprende del plan adjunto.
- **Respuesta técnica (resumen):** Una guía por tareas (P1 a P12). Para la protección de rutas propuso `@login_required` junto con `@user_passes_test` y una función `exige_staff` que lanza `PermissionDenied`; el cierre de sesión por POST; `{% csrf_token %}` en todos los formularios; y una lista blanca para el ordenamiento del catálogo.
- **Evaluación crítica:**
  1. `@user_passes_test(es_staff)` por sí solo redirige al login incluso a un usuario que ya inició sesión, pero el plan exige un 403 para el cliente sin permisos. Por eso se agregó `exige_staff`, que lanza `PermissionDenied` y deja el login solo para el anónimo.
  2. El orden de los decoradores importa: `@login_required` va primero (afuera) para filtrar al anónimo antes de evaluar el permiso.
  3. Las pruebas confirman el comportamiento: anónimo → 302 al login, cliente → 403, staff → 200, y un cliente no puede dar de baja un espectáculo con una petición POST.
- **Adaptación aplicada:** `cuentas/permisos.py` (`exige_staff`), los decoradores en las vistas de gestión de `portal/views.py` y las pruebas `cuentas/tests/test_permisos.py` y las de permisos en `portal/tests`.
- **Evidencia:** [Pull Request #2](https://github.com/Cryss0k/culturaviva/pull/2) y commit [`8732fbe`](https://github.com/Cryss0k/culturaviva/commit/8732fbedff92792a493981ed23bf240ec57d0211) (permisos de staff con respuesta 403)

#### Caso 2: Adaptación al repositorio real: validaciones, migraciones y convenciones
- **Área:** Arquitectura ORM y formularios
- **Prompt utilizado:**
  > A ver, este es el repositorio: https://github.com/Cryss0k/culturaviva

  *Contexto técnico:* integrar la parte B (apps `cuentas` y `portal`) sobre la base real del proyecto, respetando los contratos acordados entre integrantes (nombres de URL, modelos y managers), el estado de las migraciones y las convenciones del repositorio.
- **Respuesta técnica (resumen):** Claude clonó el repositorio, lo ejecutó y revisó el código existente. Ajustó la guía a lo que realmente había: la base ya traía `base.html`, los estilos y los manejadores 403/404; los nombres de las vistas ya estaban fijados en `urls.py`; el repositorio no incluía migraciones; y el campo `Perfil.rut` tenía un `TODO` para validar el RUT.
- **Evaluación crítica:**
  1. La primera guía se escribió sin ver el repositorio y contenía supuestos incorrectos: indicaba agregar `MESSAGE_TAGS` a `settings.py` (ya existía), usaba nombres de vistas distintos a los de `urls.py` y no advertía que faltaban las migraciones. Al compartir el repositorio la respuesta se corrigió; una guía generada a ciegas no puede darse por buena sin contrastarla con el código real.
  2. Había que poner `validators=[validar_rut]` en `Perfil.rut` **antes** de generar la migración de `cuentas`, para no necesitar una segunda migración.
  3. La migración de `catalogo` pertenece a otro integrante: se generó solo de forma local y no se subió, usando `git add` por archivo en vez de `git add .`.
  4. El plan indicaba manejar `ProtectedError` al eliminar; como el CRUD solo da de baja espectáculos (no elimina géneros), no aplicaba y se corrigió la documentación.
- **Adaptación aplicada:** `cuentas/validators.py` y `cuentas/models.py` (validador de RUT), `cuentas/migrations/0001_initial.py`, vistas con los nombres definidos en `urls.py`, y la corrección del apartado «Eliminar» de la sección 9.
- **Evidencia:** [Pull Request #2](https://github.com/Cryss0k/culturaviva/pull/2) y commit [`48db3d8`](https://github.com/Cryss0k/culturaviva/commit/48db3d8bc0dc17c45b61bb03c01f290fb90b0ef5) (registro con validación de RUT y migración de `cuentas`)

#### Caso 3: Búsqueda con `Q`, paginación y pruebas automáticas
- **Área:** Optimización de consultas y pruebas
- **Prompt utilizado:**
  > Okay, ahora que ya tenemos todo el panorama, dame un paso a paso de donde quedamos para verlo más detenidamente.

  *Contexto técnico:* implementar y verificar el catálogo público (búsqueda multi-campo con `Q`, filtro, ordenamiento con lista blanca y paginación que conserva los filtros) y la suite de pruebas automáticas de las apps `cuentas` y `portal`.
- **Respuesta técnica (resumen):** Claude implementó la parte B sobre una copia del repositorio y la verificó antes de entregarla: buscador multi-campo con `Q`, filtro por género, ordenamiento restringido a la lista blanca `ORDENES`, `select_related('genero')`, `Paginator` conservando la querystring, y 30 pruebas automáticas (después reorganizadas en 11 pasos con 39 pruebas).
- **Evaluación crítica:**
  1. Al ejecutar las pruebas apareció un error real: los enlaces del paginador mezclaban `&amp;` y `&` en la URL. No se veía a simple vista; lo detectó la prueba `test_paginacion_conserva_filtros` y se corrigió en `lista.html`.
  2. Aceptar cualquier campo de ordenamiento desde la URL permitiría ordenar por columnas no previstas o provocar errores; la lista blanca lo evita y un valor inválido vuelve al orden por defecto (probado con `password; DROP TABLE`).
  3. `select_related('genero')` evita una consulta adicional por cada tarjeta al mostrar el nombre del género.
  4. Verificación local: la suite se ejecutó con `python manage.py test` después de cada bloque.
- **Adaptación aplicada:** `portal/views.py` (`lista`), `portal/templates/portal/lista.html`, `templates/includes/card_espectaculo.html` y las pruebas de `portal/tests`.
- **Evidencia:** [Pull Request #2](https://github.com/Cryss0k/culturaviva/pull/2) y commit [`fd26850`](https://github.com/Cryss0k/culturaviva/commit/fd2685034c24b772c3d28bf95aefbb800af2e0f9) (catálogo con búsqueda, filtros y paginación)

#### Caso 4: Depuración de problemas de integración
- **Área:** Pruebas y depuración
- **Prompt utilizado:**
  > *(Se pegó el error `ModuleNotFoundError: No module named 'django'` al ejecutar `python manage.py migrate`.)*

  > *(Se pegó la salida de `python manage.py test cuentas portal` con `FFE....`: 2 fallos y 1 error en las pruebas de registro.)*

  > Por cual gestor lo pego? Porque me aparece `cuentas copy`, `templates copy`en el VS CODE.

  *Contexto técnico:* diagnóstico de un entorno virtual sin dependencias instaladas, de pruebas fallidas por una vista provisoria (stub) que no fue reemplazada y de carpetas duplicadas al integrar archivos.
- **Respuesta técnica (resumen):** (1) Django no estaba instalado dentro del entorno virtual: reinstalar con `python -m pip install -r requirements.txt`. (2) `resp.context` en `None` y una respuesta 200 en lugar de 302 indicaban que la vista seguía siendo el stub original, es decir, que `cuentas/views.py` no se había reemplazado. (3) Las carpetas `copy` aparecen al pegar dentro del panel de VS Code, que no mezcla carpetas; hay que pegar desde el Explorador de Windows.
- **Evaluación crítica:**
  1. El diagnóstico salió de leer el traceback y no de adivinar: `NoneType` en `resp.context` solo ocurre si no se renderizó ninguna plantilla, lo que apunta a una vista de texto plano.
  2. El problema no estaba en el código generado sino en cómo se copiaron los archivos; la guía debió advertirlo desde el principio.
  3. Tras corregir, los 7 tests del primer bloque pasaron y se comprobó con `git status` que solo se agregaran los archivos del bloque.
- **Adaptación aplicada:** Se reemplazó `cuentas/views.py` por la versión correcta, se eliminaron las carpetas `copy` y la carpeta sobrante `templates/cuentas/`, y se reinstalaron las dependencias. No hubo cambios de código.
- **Evidencia:** No aplica (problemas del entorno local, resueltos sin cambios de código).

---

## 12. Trabajo colaborativo en Git y GitHub

| Integrante | Responsabilidad |
|---|---|
| Cristian | `catalogo` (modelos, admin, `poblar_datos`) y `reservas` (carrito en sesión, comprobante) |
| Pablo | `cuentas` (autenticación y permisos) y `portal` (catálogo público, CRUD e interfaz) |

- Cada tarea se desarrolló en una rama propia (`feature/<integrante>-<descripcion>`) y se integró a `main` mediante Pull Request revisado por el otro integrante.
- Los commits siguen el formato `tipo(app): descripción` (`feat`, `fix`, `docs`, `test`, `refactor`, `chore`).
- Las normas de nomenclatura, los contratos entre módulos y el flujo de trabajo están en [`docs/GUIA_EQUIPO.md`](docs/GUIA_EQUIPO.md).
