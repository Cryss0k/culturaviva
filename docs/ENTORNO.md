# Guía de entorno y solución de problemas

## Versiones
- Python 3.12 (`python --version`)
- Dependencias fijadas en `requirements.txt`: Django 5.1.4, Pillow 11.0.0, python-dotenv 1.0.1

## Verificación rápida después de instalar
```
python --version
pip list
python manage.py check
python manage.py migrate
python manage.py test
```
`manage.py check` debe responder `System check identified no issues`.

## Variables de entorno (.env)
| Variable | Descripción | Ejemplo |
|---|---|---|
| `SECRET_KEY` | Clave secreta de Django. Debe ser larga y distinta en cada entorno | (ver comando abajo) |
| `DEBUG` | `True` solo en desarrollo | `True` |
| `ALLOWED_HOSTS` | Hosts permitidos separados por coma | `127.0.0.1,localhost` |
| `DB_NAME` | Nombre del archivo SQLite dentro de la carpeta del proyecto | `db.sqlite3` |

Generar una clave nueva:
```
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
```
El archivo `.env` está en `.gitignore`: **nunca** se sube. Lo que sí se sube es `.env.example`.

## Problemas frecuentes
| Síntoma | Causa y solución |
|---|---|
| PowerShell: "la ejecución de scripts está deshabilitada" al activar `.venv` | Ejecutar `Set-ExecutionPolicy -Scope Process Bypass` y volver a activar |
| `ModuleNotFoundError: No module named 'django'` | El `.venv` no está activo o falta `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'dotenv'` | Mismo caso: instalar dependencias dentro del `.venv` |
| `no such table` | Faltan migraciones: `python manage.py migrate` |
| `Your models have changes that are not yet reflected` | Alguien cambió modelos: `python manage.py makemigrations` y subir la migración |
| Las imágenes no se ven | Debe existir `DEBUG=True` en `.env` (las imágenes de `media/` se sirven solo en desarrollo) |

## Archivos que NO se suben a GitHub ni al .zip
`.venv/`, `__pycache__/`, `db.sqlite3`, `.env`, `media/`, `staticfiles/`.

## Generar el .zip de entrega (sin .venv ni temporales)
Linux/macOS:
```
zip -r entrega.zip . -x ".venv/*" "*/__pycache__/*" "db.sqlite3" ".env" "media/*" ".git/*"
```
Windows: comprimir la carpeta desde el explorador después de **mover o borrar** `.venv`, `db.sqlite3` y `.env` de la copia. Verificar que `.env.example` quede dentro.
