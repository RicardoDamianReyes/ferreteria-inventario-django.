from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import ProductoForm, ClienteForm
from .models import Producto, Cliente


def alerta_stock(request, producto):
    """Avisa al empleado si el producto está por agotarse."""
    if producto.stock <= 5:
        messages.warning(
            request,
            f'¡Atención! El stock de {producto.nombre} está por agotarse ({producto.stock} piezas).'
        )


# ---------- PRODUCTOS ----------

class ProductoListView(ListView):
    model = Producto
    template_name = 'tienda/producto_list.html'
    context_object_name = 'productos'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset().select_related('categoria')
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                Q(nombre__icontains=q)
                | Q(codigo_barras__icontains=q)
                | Q(categoria__nombre__icontains=q)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '').strip()
        return context


class ProductoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'tienda/form_generico.html'
    success_url = reverse_lazy('inicio')
    success_message = '¡Producto %(nombre)s registrado correctamente!'
    extra_context = {'titulo': 'Nuevo producto', 'volver': reverse_lazy('inicio')}

    def form_valid(self, form):
        response = super().form_valid(form)
        alerta_stock(self.request, self.object)
        return response


class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'tienda/form_generico.html'
    success_url = reverse_lazy('inicio')
    extra_context = {'titulo': 'Editar producto', 'volver': reverse_lazy('inicio')}

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.info(self.request, f'¡Precios/Stock de {self.object.nombre} actualizados!')
        alerta_stock(self.request, self.object)
        return response


class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = 'tienda/confirmar_eliminar.html'
    success_url = reverse_lazy('inicio')
    extra_context = {'titulo': 'Eliminar producto', 'volver': reverse_lazy('inicio')}

    def form_valid(self, form):
        messages.warning(self.request, f'El producto {self.object.nombre} fue retirado del inventario.')
        return super().form_valid(form)


# ---------- CLIENTES ----------

class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'tienda/cliente_list.html'
    context_object_name = 'clientes'


class ClienteCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'tienda/form_generico.html'
    success_url = reverse_lazy('cliente_lista')
    success_message = '¡Cliente %(nombre)s registrado correctamente!'
    extra_context = {'titulo': 'Nuevo cliente', 'volver': reverse_lazy('cliente_lista')}


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'tienda/form_generico.html'
    success_url = reverse_lazy('cliente_lista')
    extra_context = {'titulo': 'Editar cliente', 'volver': reverse_lazy('cliente_lista')}

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.info(self.request, f'¡Datos de {self.object.nombre} actualizados!')
        return response


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'tienda/confirmar_eliminar.html'
    success_url = reverse_lazy('cliente_lista')
    extra_context = {'titulo': 'Eliminar cliente', 'volver': reverse_lazy('cliente_lista')}

    def form_valid(self, form):
        messages.warning(self.request, f'El cliente {self.object.nombre} fue eliminado.')
        return super().form_valid(form)
