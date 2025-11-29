from pathlib import Path
import os
import sys
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# --- CONFIGURACIÓN DE SEGURIDAD Y ENTORNO ---
# La Secret Key se toma de las variables de entorno en producción, o usa una local segura.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-p!s4@*b8x!ufht1i+7p273nkwd02@1-ptvp8vq2un9jp2!j7fk')

# El modo DEBUG se activa automáticamente en local y se desactiva en producción.
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = []

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
else:
    # Permitir acceso local en modo desarrollo
    ALLOWED_HOSTS.append('127.0.0.1')


# --- APLICACIONES INSTALADAS ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage', # Necesario para la gestión de medios en Cloudinary
    'cloudinary',         # Necesario para la gestión de medios en Cloudinary
    'laboratorio',
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Sirve archivos estáticos eficientemente en producción
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mad_science.urls'

# --- PLANTILLAS (TEMPLATES) ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mad_science.wsgi.application'


# --- BASE DE DATOS ---
if 'RENDER' in os.environ:
    # Configuración de base de datos para PRODUCCIÓN (en Render)
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            conn_max_age=600,
            ssl_require=True # Render requiere conexiones SSL
        )
    }
    # Asegura la codificación correcta para acentos y caracteres especiales
    DATABASES['default']['OPTIONS'] = {'client_encoding': 'UTF8'}
else:
    # Configuración de base de datos para DESARROLLO LOCAL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'iqs_db',
            'USER': 'postgres',
            'PASSWORD': 'root', # <-- ¡¡¡CAMBIA ESTO!!!
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }


# --- VALIDACIÓN DE CONTRASEÑAS ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --- INTERNACIONALIZACIÓN ---
LANGUAGE_CODE = 'es-cl' # Cambiado a español de Chile
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True


# --- ARCHIVOS ESTÁTICOS (STATIC FILES) ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [ BASE_DIR / 'laboratorio/static' ]
# En producción, WhiteNoise necesita una carpeta donde recoger todos los estáticos.
if not DEBUG:
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# --- ARCHIVOS MULTIMEDIA (MEDIA FILES) ---
MEDIA_URL = '/media/'

# Configuración de Cloudinary para almacenar los archivos subidos por el usuario
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

if 'RENDER' in os.environ:
    # En producción, usa Cloudinary como sistema de almacenamiento por defecto.
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    # En local, guarda los archivos en una carpeta 'media' en tu disco duro.
    MEDIA_ROOT = BASE_DIR / 'media'


# --- CONFIGURACIONES ADICIONALES DEL PROYECTO ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

LOGIN_REDIRECT_URL = 'laboratorio:lista_inventos'
LOGOUT_REDIRECT_URL = 'login'