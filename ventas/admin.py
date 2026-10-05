from django.contrib import admin

from .models import Carrito, ItemCarrito, ItemOrden, Orden


class ItemCarritoInline(admin.TabularInline):
    model = ItemCarrito
    extra = 0


class ItemOrdenInline(admin.TabularInline):
    model = ItemOrden
    extra = 0


@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "estado", "actualizado")
    list_filter = ("estado",)
    inlines = [ItemCarritoInline]


@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ("carrito", "lugar", "cantidad")


@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre_cliente", "total", "estado", "creada")
    list_filter = ("estado",)
    inlines = [ItemOrdenInline]


@admin.register(ItemOrden)
class ItemOrdenAdmin(admin.ModelAdmin):
    list_display = ("orden", "nombre_lugar", "precio_unitario", "cantidad")
