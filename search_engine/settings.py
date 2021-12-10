from pathlib import Path
import os, ast

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'main.apps.MainConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "corsheaders",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "htmlmin.middleware.HtmlMinifyMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    "django.contrib.admindocs.middleware.XViewMiddleware",
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django.middleware.cache.FetchFromCacheMiddleware",
    "htmlmin.middleware.MarkRequestMiddleware",
]

ROOT_URLCONF = 'search_engine.urls'

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

WSGI_APPLICATION = 'search_engine.wsgi.application'


dotenv_file = BASE_DIR / ".env"
if os.path.isfile(dotenv_file):
    import dotenv

    dotenv.load_dotenv(dotenv_file)

    PRODUCTION_SERVER = False
    DEBUG = ast.literal_eval(os.environ.get("DEBUG", "True").capitalize())
    SECRET_KEY = 'django-insecure-keb*=hj$2$k%9$5k#916t0d(8_-0tm6mbtb+))2&j)hlv03paw'
    CACHE_MIDDLEWARE_SECONDS = 0
    LOCAL = True
else:
    LOCAL = ast.literal_eval(os.environ.get("LOCAL", "False"))
    PRODUCTION_SERVER = True
    DEBUG = ast.literal_eval(os.environ.get("DEBUG", "False").capitalize())
    SECRET_KEY = os.environ.get("SECRET_KEY", "SECRET_KEY")

if os.getenv("DATABASE_URL"):
    import dj_database_url
    DATABASES = {
        "default": dj_database_url.config(default=os.getenv("DATABASE_URL"))
    }
else:
    raise RuntimeError('DATABASE_URL is not set in environment variable')

if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


if not os.getenv("WHITENOISE"):
    MIDDLEWARE = ([MIDDLEWARE[0]] +
                  ["whitenoise.middleware.WhiteNoiseMiddleware"] +
                  MIDDLEWARE[1:])
    INSTALLED_APPS = (INSTALLED_APPS[0:-1] + [
        "whitenoise.runserver_nostatic",
    ] + [INSTALLED_APPS[-1]])


if PRODUCTION_SERVER:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_REFERRER_POLICY = "same-origin"
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Calcutta'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # "compressor.finders.CompressorFinder",
]

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

WHITENOISE_MAX_AGE = 9000
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = []

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
]
ALLOWED_HOSTS = ['*']
CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS  = [
    "http://localhost:8080",
    "http://127.0.0.1:9000",
    "http://127.0.0.1:8000",    
]

COMPRESS_ENABLED = ast.literal_eval(os.environ.get("COMPRESS_ENABLED", "True"))
COMPRESS_OFFLINE = ast.literal_eval(os.environ.get("COMPRESS_OFFLINE", "True"))
COMPRESS_PRECOMPILERS = (
    ("text/x-sass", "django_libsass.SassCompiler"),
    ("text/x-scss", "django_libsass.SassCompiler"),
)
COMPRESS_CSS_HASHING_METHOD = "content"
# COMPRESS_FILTERS = {
#     "css": [
#         "compressor.filters.css_default.CssAbsoluteFilter",
#         "compressor.filters.cssmin.rCSSMinFilter",
#     ],
#     "js": [
#         "compressor.filters.jsmin.JSMinFilter",
#     ],
# }
HTML_MINIFY = True
KEEP_COMMENTS_ON_MINIFYING = False

SESSION_COOKIE_AGE = 1 * 60 * 60
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
