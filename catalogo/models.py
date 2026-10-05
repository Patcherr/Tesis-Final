from django.db import models
from django.urls import reverse


class Lugar(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to="lugares/")
    precio_entrada = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "lugar"
        verbose_name_plural = "lugares"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("catalogo:detalle", kwargs={"slug": self.slug})
