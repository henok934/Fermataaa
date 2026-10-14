import os
from pathlib import Path

# 1. BASE DIRECTORY DEFINED FIRST
BASE_DIR = Path(__file__).resolve().parent.parent
from dotenv import load_dotenv

load_dotenv(os.path.join(BASE_DIR, '.env'))
# 2. SECURITY SETTINGS (Production Grade)
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your-default-secret-key')
# settings.py ውስጥ
DEBUG = True  # <-- ወደ False ይለውጡት
ALLOWED_HOSTS = [
    'fermataa-3ooq.onrender.com',
    'wedehagertransport.onrender.com',
    '.onrender.com',
    'value-shortly-unveiled.ngrok-free.dev',
    'localhost',
    '127.0.0.1'
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,  # የይለፍ ቃሉ ቢያንስ 8 ቁጥሮች/ፊደላት መሆን አለበት
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Security Headers
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# Strict Transport Security (HSTS) - 1 Year
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

REFERRER_POLICY = 'same-origin'

# Cookie Security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
# settings.py

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 1209600  # ለ 2 ሳምንት ይቆያል
SESSION_SAVE_EVERY_REQUEST = True

# 3. APPLICATION DEFINITION
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third Party Apps
    'rest_framework',
    'drf_spectacular',
    'corsheaders',
    'axes',
    'csp',    
    # Your Apps
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'csp.middleware.CSPMiddleware', # <-- CSP Middleware በትክክል ተቀምጧል
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
]


# Content Security Policy Settings (CSP)
# --- አዲሱ የ CSP 4.0+ ውቅር ---
# Content Security Policy Settings (CSP)
PERMISSIONS_POLICY = {
    "geolocation": [],
    "camera": [],
    "microphone": [],
}


# Content Security Policy Settings (CSP)
"""
CONTENT_SECURITY_POLICY = {
    'DIRECTIVES': {
        'default-src': ("'self'", 'https:', 'data:'),
        'img-src': ("'self'", 'data:', 'https:'),
        'script-src': ("'self'", "'unsafe-inline'", "'unsafe-eval'", 'https://code.jquery.com', 'https://stackpath.bootstrapcdn.com', 'https://translate.google.com', 'https://translate.googleapis.com', 'https://challenges.cloudflare.com', 'https://*.cloudflare.com'),
        'style-src': ("'self'", "'unsafe-inline'", 'https://fonts.googleapis.com', 'https://cdnjs.cloudflare.com', 'https://stackpath.bootstrapcdn.com'),
        'font-src': ("'self'", 'https://fonts.gstatic.com', 'https://cdnjs.cloudflare.com'),
        'connect-src': ("'self'", 'https://challenges.cloudflare.com', 'https://*.cloudflare.com', 'https://translate.googleapis.com'),
        'frame-src': ("'self'", 'https://challenges.cloudflare.com', 'https://*.cloudflare.com', 'https://translate.google.com'),
    }
}
"""
CONTENT_SECURITY_POLICY = {
    'DIRECTIVES': {
        'default-src': ("'self'", 'https:', 'data:'),
        'img-src': ("'self'", 'data:', 'https:'),
        'script-src': (
            "'self'",
            "'unsafe-inline'",
            "'unsafe-eval'",
            'https://code.jquery.com',
            'https://stackpath.bootstrapcdn.com',
            'https://translate.google.com',
            'https://translate.googleapis.com',
            'https://challenges.cloudflare.com',
            'https://*.cloudflare.com',
            'https://*.ethiotelecom.et',  # <-- የ Telebirr Script ለማስፈቀድ
            'https://developerportal.ethiotelecom.et:38443',
        ),
        'style-src': (
            "'self'",
            "'unsafe-inline'",
            'https://fonts.googleapis.com',
            'https://cdnjs.cloudflare.com',
            'https://stackpath.bootstrapcdn.com'
        ),
        'font-src': (
            "'self'",
            'https://fonts.gstatic.com',
            'https://cdnjs.cloudflare.com'
        ),
        'connect-src': (
            "'self'",
            'https://challenges.cloudflare.com',
            'https://*.cloudflare.com',
            'https://translate.googleapis.com',
            'https://*.ethiotelecom.et',  # <-- Telebirr API request ለማድረግ
            'https://developerportal.ethiotelecom.et:38443',
        ),
        'frame-src': (
            "'self'",
            'https://challenges.cloudflare.com',
            'https://*.cloudflare.com',
            'https://translate.google.com',
            'https://*.ethiotelecom.et',  # <-- Telebirr Payment iframe/page ለማሳየት
            'https://developerportal.ethiotelecom.et:38443',
        ),
        'form-action': (
            "'self'",
            'https://*.ethiotelecom.et',  # <-- ከ Form ቀጥታ ወደ Telebirr Redirect ከተደረገ እንዳይከለክል
            'https://developerportal.ethiotelecom.et:38443',
        ),
    }
}

ROOT_URLCONF = 'myproje.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'users/templates')],
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

WSGI_APPLICATION = 'myproje.wsgi.application'

# 4. DATABASE

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',

        'OPTIONS': {
            'timeout': 20,
    }
}
}

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'my_app_db',
        'USER': 'data',
        'PASSWORD': 'Teklu@934',
        'HOST': 'localhost',
        'PORT': '5432',

        'CONN_MAX_AGE': 600,
    }
}
"""

# 5. AUTHENTICATION & USERS
AUTH_USER_MODEL = 'users.CustomUser'
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

#AXES_ENABLED = False
AXES_ENABLED = True
# 6. EMAIL SETTINGS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'teklemariammossie1@gmail.com'
EMAIL_HOST_PASSWORD = 'xbbdaymgoqapntds'
DEFAULT_FROM_EMAIL = 'teklemariammossie697@gmail.com'

# 7. STATIC & MEDIA FILES
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'users/static')]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 8. CORS & CSRF
#CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_ALL_ORIGINS = False
CSRF_TRUSTED_ORIGINS = [
    'https://wedehagertransport.onrender.com',
    'https://fermataa-3ooq.onrender.com',
    'https://value-shortly-unveiled.ngrok-free.dev',
]
CORS_ALLOWED_ORIGINS = [
    'https://wedehagertransport.onrender.com',
    'https://fermataa-3ooq.onrender.com',
    'https://value-shortly-unveiled.ngrok-free.dev',
]
# 9. INTERNATIONALIZATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Addis_Ababa'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
    'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
    'anon': '100/minute',  # 👈 ከ 5/minute ወደ 100/minute ቀይረው
    }
}

# ==========================================
# AXES CONFIGURATION (ለ Development የሚሆን)
# ==========================================
AXES_FAILURE_LIMIT = 20         # ሎጊን የመሳሳት ገደቡን ከ 3 ወደ 20 ከፍ ያደርገዋል
AXES_COOLOFF_TIME = 0.05        # የታገደ አካውንት ከ 3 ደቂቃ በኋላ በራሱ እንዲከፈት ያደርጋል
AXES_RESET_ON_SUCCESS = True     # ትክክለኛ የይለፍ ቃል ሲገባ የተሳሳቱ ሙከራዎችን ያጸዳል


raw_private_key = os.environ.get("TELEBIRR_PRIVATE_KEY", "")
raw_public_key = os.environ.get("TELEBIRR_PUBLIC_KEY", "")
notify_url_env = os.environ.get("TELEBIRR_NOTIFY_URL", "").strip()
redirect_url_env = os.environ.get("TELEBIRR_REDIRECT_URL", "").strip()
TELEBIRR_CONFIG = {
     "BASE_URL": os.environ.get(
        "TELEBIRR_BASE_URL", "https://developerportal.ethiotelecom.et:38443"
    ),
    "WEB_BASE_URL": os.environ.get(
        "TELEBIRR_WEB_BASE_URL",
        "https://developerportal.ethiotelecom.et:38443/pay/",
    ),

    "merchantCode": os.environ.get("TELEBIRR_MERCHANT_CODE", "259159"),
    "merchantAppId": os.environ.get(
        "TELEBIRR_MERCHANT_APP_ID", "1674185087411200"
    ),
    "fabricAppId": os.environ.get(
        "TELEBIRR_FABRIC_APP_ID", "c4182ef8-9249-458a-985e-06d191f4d505"
    ),
    "appSecret": os.environ.get(
        "TELEBIRR_APP_SECRET", "fad0f06383c6297f545876694b974599"
    ),

    "notify_url": os.environ.get("TELEBIRR_NOTIFY_URL", "https://value-shortly-unveiled.ngrok-free.dev/api/telebirr/callback/"),
    "redirect_url": os.environ.get("TELEBIRR_REDIRECT_URL", "https://value-shortly-unveiled.ngrok-free.dev/users/telebirr-redirect/"),
    "PRIVATE_KEY": raw_private_key.replace("\\n", "\n") if raw_private_key else "",
    "PUBLIC_KEY": raw_public_key.replace("\\n", "\n") if raw_public_key else "",
}
# settings10.py ላይ የነበረው
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
