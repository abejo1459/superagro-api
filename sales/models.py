from django.db import models
from users.models import Usuario
from inventory.models import Producto

class Venta(models.Model):
    FORMAS_PAGO = (
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta'),
        ('TRANSFERENCIA', 'Transferencia'),
    )
    
    vendedor = models.ForeignKey(Usuario, on_delete=models.RESTRICT, limit_choices_to={'rol': 'VENDEDOR'})
    fecha = models.DateTimeField(auto_now_add=True)
    forma_pago = models.CharField(max_length=20, choices=FORMAS_PAGO)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Venta {self.id} - Vendedor: {self.vendedor.username}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Lógica para la HU-003: Descuento automático de inventario
        if not self.pk:  # Si es un registro nuevo
            if self.producto.stock >= self.cantidad:
                self.producto.stock -= self.cantidad
                self.producto.save()
            else:
                raise ValueError(f"Stock insuficiente para el producto {self.producto.nombre}")
        
        super().save(*args, **kwargs)