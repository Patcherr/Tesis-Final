from django.contrib import admin

from .models import Lugar


@admin.register(Lugar)
class LugarAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio_entrada", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre",)
    prepopulated_fields = {"slug": ("nombre",)}
