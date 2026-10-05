from django.contrib import admin

from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("user", "dni", "telefono", "ciudad")
    search_fields = ("user__username", "user__email", "dni")
