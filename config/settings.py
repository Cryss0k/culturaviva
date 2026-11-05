"""Configuración de CulturaViva Producciones.

Las variables sensibles se leen desde .env (python-dotenv). Ver .env.example.
Este archivo es compartido: cambios solo mediante PR pequeño y aviso al equipo.
"""
import os
from decimal import Decimal
from pathlib import Path

from django.contrib.messages import constants as messages_constants
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

# --- Seguridad y entorno -----------------------------------------------------
SECRET_KEY = os.getenv('SECRET_KEY', 'clave-insegura-solo-desarrollo')
DEBUG = os.getenv('DEBUG', 'False').strip().lower() in ('1', 'true', 'yes')
ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',') if h.strip()]

# --- Aplicaciones -------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps del proyecto
    'catalogo',   # Cristian: modelos, admin, poblar_datos
    'reservas',   # Cristian: carrito en sesión
    'cuentas',    # Pablo: registro, login, perfil, permisos
    'portal',     # Pablo: catálogo público y CRUD de gestión
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'reservas.context_processors.carrito_contador',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# --- Base de datos -------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / os.getenv('DB_NAME', 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internacionalización -------------------------------------------------------
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# --- Archivos estáticos y multimedia -----------------------------------------
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Autenticación ------------------------------------------------------------
LOGIN_URL = 'cuentas:login'
LOGIN_REDIRECT_URL = 'portal:inicio'
LOGOUT_REDIRECT_URL = 'portal:inicio'

# --- Mensajes (Bootstrap usa 'danger' en vez de 'error') ----------------------
MESSAGE_TAGS = {messages_constants.ERROR: 'danger'}

# --- Reglas de negocio del carrito de entradas --------------------------------
RECARGO_SERVICIO_PORCENTAJE = Decimal('0.10')
IVA_PORCENTAJE = Decimal('0.19')
MAX_ENTRADAS_POR_COMPRA = 6
