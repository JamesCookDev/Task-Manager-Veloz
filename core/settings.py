import os
from pathlib import Path
import dotenv
from datetime import timedelta



BASE_DIR = Path(__file__).resolve().parent.parent

dotenv.load_dotenv(os.path.join(BASE_DIR, '.env'))




SECRET_KEY = os.environ.get('SECRET_KEY')


DEBUG = os.environ.get('DEBUG') == 'True'


ALLOWED_HOSTS = []



INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'rest_framework',
    'corsheaders',
    'drf_spectacular',
    'rest_framework_simplejwt',
    'djangogrpcframework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'HOST' : os.environ.get('DB_HOST'),
        'PORT' : os.environ.get('DB_PORT'),
    }
}



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



LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True




STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

cors_allowed_origins_csv = os.environ.get('CORS_ALLOWED_ORIGINS')
if cors_allowed_origins_csv:
    CORS_ALLOWED_ORIGINS = cors_allowed_origins_csv.split(',')
else:
    CORS_ALLOWED_ORIGINS = []


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'API do gerenciador de tarefas',
    'DESCRIPTION': 'Documentação detalhada da API para o projeto Gerenciador de Tarefas da Veloz.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}


JAZZMIN_SETTINGS = {
    "site_title": "Gerenciador de Tarefas",
    "site_header": "Gerenciador de Tarefas",
    "site_brand": "Gerenciador de Tarefas",
    "welcome_sign": "Bem-vindo ao Gerenciador de Tarefas",
    "copyright": "Gerenciador de Tarefas",
    "search_model": ["auth.User", "app.Project", "app.Task"],
    "order_with_respect_to": ["auth", "app", "app.Project", "app.Task"],
    
    "show_sidebar": True,
    "navigation_expanded": True,
    "changeform_format": "horizontal_tabs",
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=90),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=180),
}

GRPC_FRAMEWORK = {
    'ROOT_HANDLERS': [
        'app.services',
    ],
}