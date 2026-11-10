from django.contrib import admin
from .models import Categoria, Producto, Cliente


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ("nombre",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "precio", "stock", "codigo_barras")
    list_filter = ("categoria",)
    search_fields = ("nombre", "codigo_barras")


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "telefono", "correo", "direccion")
    search_fields = ("nombre", "correo")
