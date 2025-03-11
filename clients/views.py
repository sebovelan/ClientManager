from calendar import month
from rest_framework import generics
from rest_framework.response import Response
from .models import Client
from .serializers import ClientSerializer
from django.shortcuts import render


def get_clients(request):  # Simple name, no "home"
    total_clients = Client.objects.count()  # Like "client.count"
    return render(request, 'index.html', {'total_clients': total_clients})
# Alta (Create)
class ClientCreateView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def perform_create(self, serializer):
        serializer.save()

# Baja (Delete - Soft)
class ClientDeleteView(generics.UpdateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def update(self, request, *args, **kwargs):
        client = self.get_object()
        client.status = 'inactive'
        client.save()
        return Response({'message': 'Cliente dado de baja'})

# Modificación (Update)
class ClientUpdateView(generics.UpdateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def update(self, request, *args, **kwargs):
        client = self.get_object()
        serializer = self.get_serializer(client, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Cliente modificado', 'client': serializer.data})

# Read (List and Detail)
class ClientListView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ClientDetailView(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer



