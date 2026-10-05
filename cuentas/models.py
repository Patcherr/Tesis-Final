from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models


class Cliente(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cliente"
    )
    dni = models.CharField(
        max_length=8,
        unique=True,
        validators=[RegexValidator(r"^\d{7,8}$", "El DNI debe tener 7 u 8 dígitos numéricos.")],
    )
    telefono = models.CharField(max_length=20, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    ciudad = models.CharField(max_length=80, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.get_username()
