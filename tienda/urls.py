from django.db.models import Q
from django.views.generic import ListView
from .models import Producto


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