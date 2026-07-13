from rest_framework import viewsets, permissions
from .models import Venta
from .serializers import VentaSerializer

class PermisosVentas(permissions.BasePermission):
    def has_permission(self, request, view):
        # Just Admin and Vendedor can process or see ventas module
        return request.user.rol in ['ADMIN', 'VENDEDOR']

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [PermisosVentas]