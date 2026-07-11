from rest_framework import serializers
from .models import Venta, DetalleVenta

class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad', 'precio_unitario']

class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True)

    class Meta:
        model = Venta
        fields = ['id', 'vendedor', 'fecha', 'forma_pago', 'total', 'detalles']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        venta = Venta.objects.create(**validated_data)
        
        # Guardar cada detalle de la venta (esto disparará el descuento del stock)
        for detalle_data in detalles_data:
            DetalleVenta.objects.create(venta=venta, **detalle_data)
            
        return venta