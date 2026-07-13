from rest_framework import viewsets, filters, permissions
from rest_framework.response import Response
from .models import Categoria, Producto
from .serializers import CategoriaSerializer, ProductoSerializer

class PermisosInventario(permissions.BasePermission):
    def has_permission(self, request, view):
        # Everyone authenticated can READ (GET)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Just ADMIN can CREATE (POST) or DELETE
        if request.method in ['POST', 'DELETE']:
            return request.user.rol == 'ADMIN'
        # ADMIN and ALMACENISTA can UPDATE (PUT, PATCH)
        if request.method in ['PUT', 'PATCH']:
            return request.user.rol in ['ADMIN', 'ALMACENISTA']
        return False

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'codigo']
    permission_classes = [PermisosInventario] 

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Copy sent data to handle them
        data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
        
        # HU-005: Si es ALMACENISTA, forzamos que solo se lea el campo 'stock'
        if request.user.rol == 'ALMACENISTA':
            data = {'stock': request.data.get('stock', instance.stock)}
            partial = True # Force True to do not ask for mandatory fields
            
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticated]