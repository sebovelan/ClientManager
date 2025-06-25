# clientSystem/urls.py
from django.contrib import admin
from django.urls import path, include

# Import Spectacular views for API documentation
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls), # Django Admin interface
    path('', include('clients.urls')), # Include URLs from your 'clients' app

    # --- DRF SPECTACULAR API DOCUMENTATION URLs ---
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'), # OpenAPI schema in JSON/YAML
    # Swagger UI (interactive API documentation)
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Redoc (alternative API documentation UI)
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]