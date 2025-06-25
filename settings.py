# clientSystem/settings.py

from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta # Added for SIMPLE_JWT config

# Load environment variables from a .env file (for local development only)
# IMPORTANT: In production, these variables MUST be injected by your deployment system.
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# --- CRITICAL SECURITY SETTINGS (for Production Readiness) ---
# 1. SECRET_KEY: NEVER use a fallback or a default value in production.
#    It must be provided via environment variable, or the app should fail to start.
#    Generate a very long, complex key for production:
#    (e.g., in Python shell: from django.core.management.utils import get_random_secret_key; print(get_random_secret_key()))
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY environment variable not set. This is critical for security.")

# 2. DEBUG: Must be False in production. Control with an environment variable.
DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() == 'true'

# 3. ALLOWED_HOSTS: Must be set in production when DEBUG is False.
#    List the domains and/or IP addresses from which your application will be served.
#    Example: ['api.yourcompany.com', 'your_server_ip']
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')
if not DEBUG and not ALLOWED_HOSTS:
    raise ValueError("ALLOWED_HOSTS must be set in production when DEBUG is False to prevent Host header attacks.")


# --- APPLICATION DEFINITION ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps:
    'rest_framework',         # Django REST Framework core
    'rest_framework_simplejwt', # For JWT (JSON Web Token) authentication
    'corsheaders',            # For Cross-Origin Resource Sharing (CORS) management
    'drf_spectacular',        # For OpenAPI Schema and API documentation (Swagger UI / Redoc)

    # Your project apps:
    'clients',
]

# --- MIDDLEWARE CONFIGURATION ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # CORS middleware MUST come before CommonMiddleware
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'clientSystem.urls'

# --- DJANGO REST FRAMEWORK (DRF) SETTINGS ---
REST_FRAMEWORK = {
    # Default Authentication Classes:
    # JWTAuthentication for stateless API communication (recommended for professional APIs).
    # SessionAuthentication is kept for Django Admin access if served from the same instance.
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    # Default Permission Classes:
    # IsAdminUser: Only Django Admin (staff) users can access the API.
    # If the API is for any authenticated user (not just staff), use 'rest_framework.permissions.IsAuthenticated'.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
        # 'rest_framework.permissions.IsAuthenticated', # Uncomment if general authenticated users should access
    ),
    # Optional: Global Pagination Configuration (helps with scalability for list views)
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10, # Number of items per page by default
}

# --- DJANGO REST FRAMEWORK SIMPLE JWT (JWT) CONFIGURATION ---
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),    # Short lifespan for access tokens (security)
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),      # Longer lifespan for refresh tokens
    'ROTATE_REFRESH_TOKENS': True,                    # Generate a new refresh token on refresh
    'BLACKLIST_AFTER_ROTATION': True,                 # Invalidate old refresh tokens
    'UPDATE_LAST_LOGIN': True,                        # Update user's last_login field on token refresh

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY, # Reuses Django's SECRET_KEY for JWT signing
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# --- CORS HEADERS CONFIGURATION ---
# For Cross-Origin Resource Sharing. Essential if your frontend is on a different domain.
# IMPORTANT: In production, NEVER use CORS_ALLOW_ALL_ORIGINS = True.
# Explicitly list your frontend domains here.
CORS_ALLOWED_ORIGINS = [
    # "https://yourfrontend.com", # Example for production
    # "http://localhost:3000",    # Example for local frontend development (e.g., React/Vue)
]
# For development, you can allow all origins (only if DEBUG is True)
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True


# --- DRF SPECTACULAR (OpenAPI/Swagger) SETTINGS ---
# https://drf-spectacular.readthedocs.io/en/latest/settings.html
SPECTACULAR_SETTINGS = {
    'TITLE': 'Client Management API',
    'DESCRIPTION': 'API for managing client information, including CRUD and soft-delete operations.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False, # Schema is served at /api/schema/
    # 'SERVE_PUBLIC': False, # Optional: Set to True to restrict schema to authenticated users
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"], # Path to your main templates directory
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

WSGI_APPLICATION = 'clientSystem.wsgi.application'


# --- DATABASE CONFIGURATION ---
# Use PostgreSQL in production. Credentials loaded from environment variables.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),        # No fallback; must be set in env for prod
        'USER': os.getenv('DB_USER'),        # No fallback; must be set in env for prod
        'PASSWORD': os.getenv('DB_PASSWORD'),# No fallback; must be set in