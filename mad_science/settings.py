from pathlib import Path
import os
from django.contrib.messages import constants as messages
from decouple import config, Csv  # Para leer archivo .env
import dj_database_url           # Para configurar la BD automáticamente

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
#  CONFIGURACIÓN SEGURA (Lée desde el archivo .env)
# ==============================================================================

# Si no encuentra SECRET_KEY en el .env, usa una por defecto (solo para que no falle en local si olvidas el .env)
SECRET_KEY = config('SECRET_KEY', default='django-insecure-fallback-dev-key')

# DEBUG ahora es Falso por defecto, a menos que el .env diga lo contrario
DEBUG = config('DEBUG', default=False, cast=bool)

# Lee los hosts permitidos separados por coma
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())

# ==============================================================================
#  APPLICACIONES
# ==============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'laboratorio',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware", # <--- NUEVO: Para servir CSS en producción
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mad_science.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mad_science.wsgi.application'

# ==============================================================================
#  BASE DE DATOS DINÁMICA
# ==============================================================================

# Aquí ocurre la magia:
# 1. Busca la variable DATABASE_URL en el archivo .env
# 2. Si no la encuentra (default), usa tu configuración local de PostgreSQL
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='postgres://postgres:root@localhost:5432/iqs_db')
    )
}

# ==============================================================================
#  VALIDACIÓN DE PASSWORD
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ==============================================================================
#  IDIOMA Y ZONA HORARIA
# ==============================================================================

LANGUAGE_CODE = 'es-es' # Cambiado a español

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# ==============================================================================
#  ARCHIVOS ESTÁTICOS (CSS, JS, IMAGES)
# ==============================================================================

STATIC_URL = 'static/'

# Carpeta donde se recolectarán los estilos para producción
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configuración de WhiteNoise para optimizar la carga de archivos
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Configuración de archivos subidos por el usuario (Fotos)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ==============================================================================
#  CONFIGURACIONES EXTRA
# ==============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# Redirección con el namespace correcto
LOGIN_REDIRECT_URL = 'laboratorio:lista_inventos'
LOGOUT_REDIRECT_URL = 'login'