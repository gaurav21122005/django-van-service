from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ================= SECURITY =================
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-vanservice-dev-key-change-in-production"
)

DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = ["*"]  # for Render (you can restrict later)

# ================= APPS =================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'tracking',
]

# ================= MIDDLEWARE =================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # 🔥 for static files on Render
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vanservice.urls'

# ================= TEMPLATES =================
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

WSGI_APPLICATION = 'vanservice.wsgi.application'

# ================= DATABASE =================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ================= VALIDATORS =================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ================= INTERNATIONAL =================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ================= STATIC FILES (FIXED FOR RENDER) =================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# ================= WHITE NOISE (PRODUCTION STATIC) =================
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ================= DEFAULT =================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
