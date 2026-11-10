from django.views.generic import ListView
from .models import Producto


class ProductoListView(ListView):
    model = Producto
    template_name = 'tienda/producto_list.html'
    context_object_name = 'productos'
