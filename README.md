# CulturaViva Producciones

Plataforma web de una productora de eventos y cultura, desarrollada con Django.
Evaluación Sumativa N° 3 · Programación Back End (T13041) · Unidad 2: Framework Back End.

## Ficha de registro de la propuesta

| Campo | Valor |
|---|---|
| Nombre de la organización o plataforma | CulturaViva Producciones |
| Modelo de negocio / giro | Productora de eventos y espectáculos culturales con venta de entradas |
| Integrantes del equipo | Cristian [RUT] · Pablo [RUT] |
| Entidad de contexto / agrupación (ORM) | `Genero` (Teatro, Música, Danza, Stand-up...) |
| Entidad principal gestionable (ORM) | `Espectaculo` |
| Propósito de la sesión (`request.session`) | Carrito de entradas con reserva temporal, recargo por servicio (10%) e IVA (19%) |

## Instalación paso a paso

Requisitos: Python 3.12 y Git.

**Windows (PowerShell)**
```
git clone <URL_DEL_REPOSITORIO>
cd culturaviva
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python manage.py makemigrations catalogo cuentas   # solo si aún no hay migraciones en el repo
python manage.py migrate
python manage.py poblar_datos
python manage.py runserver
```

**Linux / macOS**
```
git clone <URL_DEL_REPOSITORIO>
cd culturaviva
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations catalogo cuentas   # solo si aún no hay migraciones en el repo
python manage.py migrate
python manage.py poblar_datos
python manage.py runserver
```

Datos mínimos de prueba (antes de que exista `poblar_datos`): `python manage.py loaddata fixtures/demo_minimo.json`

Pruebas: `python manage.py test`

Guía detallada, variables de `.env` y solución de problemas: [`docs/ENTORNO.md`](docs/ENTORNO.md)

## Credenciales de prueba
_(Completar cuando `poblar_datos` esté implementado)_

| Rol | Usuario | Contraseña |
|---|---|---|
| Administrador (staff) | admin | _por definir_ |
| Cliente | cliente | _por definir_ |

## Estructura del proyecto
Ver `docs/GUIA_EQUIPO.md` (reparto por apps, normas, contratos y flujo de trabajo).

## Documentación por integrante

### Cristian: base de datos, Admin y sesión
_(Completar: modelo de datos, comando `poblar_datos`, configuración del Admin, funcionamiento del carrito.)_

#### Bitácora de prompts de IA: Cristian
_(Mínimo 3 casos. Usar la plantilla de abajo.)_

### Pablo: CRUD, autenticación y seguridad
_(Completar: rutas, roles, validaciones, protección de rutas y CSRF.)_

#### Bitácora de prompts de IA: Pablo
_(Mínimo 3 casos. Usar la plantilla de abajo.)_

### Plantilla de caso de bitácora
```
### Caso N: [título breve]
- Autor:
- Herramienta (ChatGPT / Claude / Gemini / Copilot):
- Área (arquitectura ORM / consultas / seguridad):
- Prompt utilizado:
- Respuesta técnica (resumen):
- Evaluación crítica (qué estaba bien y qué no):
- Adaptación aplicada (archivo y motivo):
- Evidencia (commit o PR):
```
