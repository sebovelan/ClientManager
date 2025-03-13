from django.urls import path
from . import views


urlpatterns = [
    path('clients/', views.ClientListView.as_view(), name='client-list'),
    path('clients/add/', views.ClientCreateView.as_view(), name='client-create'),  # Alta
    path('clients/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client-delete'),  # Baja
    path('clients/<int:pk>/update/', views.ClientUpdateView.as_view(), name='client-update'),  # Modificación
    path('clients/<int:pk>/', views.ClientDetailView.as_view(), name='client-detail'),
    path('', views.index, name='index'),
]