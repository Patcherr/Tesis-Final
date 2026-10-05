from django.db import models
from django.db.models import Q

from catalogo.models import Lugar
from cuentas.models import Cliente


class Carrito(models.Model):
    class Estado(models.TextChoices):
        ABIERTO = "abierto", "Abierto"
        CONVERTIDO = "convertido", "Convertido en orden"

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="carritos")
    estado = models.CharField(max_length=12, choices=Estado.choices, default=Estado.ABIERTO)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            # Un solo carrito abierto por cliente.
            models.UniqueConstraint(
                fields=["cliente"],
                condition=Q(estado="abierto"),
                name="un_carrito_abierto_por_cliente",
            ),
        ]

    def __str__(self):
        return f"Carrito {self.pk} de {self.cliente}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="items")
    lugar = models.ForeignKey(Lugar, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["carrito", "lugar"], name="un_item_por_lugar_en_carrito"),
            models.CheckConstraint(condition=Q(cantidad__gte=1), name="item_carrito_cantidad_minima"),
        ]

    def __str__(self):
        return f"{self.cantidad} x {self.lugar}"

    @property
    def subtotal(self):
        return self.lugar.precio_entrada * self.cantidad


class Orden(models.Model):
    class Estado(models.TextChoices):
        CONFIRMADA = "confirmada", "Confirmada"
        CANCELADA = "cancelada", "Cancelada"

    cliente = models.ForeignKey(
        Cliente, on_delete=models.SET_NULL, null=True, related_name="ordenes"
    )
    nombre_cliente = models.CharField(max_length=150)  # copia histórica
    email_cliente = models.EmailField()  # copia histórica
    total = models.DecimalField(max_digits=12, decimal_places=2)
    estado = models.CharField(max_length=12, choices=Estado.choices, default=Estado.CONFIRMADA)
    creada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creada"]
        verbose_name_plural = "órdenes"

    def __str__(self):
        return f"Orden {self.pk} - {self.nombre_cliente}"


class ItemOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name="items")
    lugar = models.ForeignKey(Lugar, on_delete=models.PROTECT)
    nombre_lugar = models.CharField(max_length=120)  # copia histórica
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)  # copia histórica
    cantidad = models.PositiveIntegerField()

    class Meta:
        verbose_name = "item de orden"
        verbose_name_plural = "items de orden"

    def __str__(self):
        return f"{self.cantidad} x {self.nombre_lugar}"

    @property
    def subtotal(self):
        return self.precio_unitario * self.cantidad
