from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductoListView.as_view(), name='inicio'),
    path('inventario/nuevo/', views.ProductoCreateView.as_view(), name='producto_crear'),
    path('inventario/<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='producto_editar'),
    path('inventario/<int:pk>/eliminar/', views.ProductoDeleteView.as_view(), name='producto_eliminar'),
    path('clientes/', views.ClienteListView.as_view(), name='cliente_lista'),
    path('clientes/nuevo/', views.ClienteCreateView.as_view(), name='cliente_crear'),
    path('clientes/<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='cliente_editar'),
    path('clientes/<int:pk>/eliminar/', views.ClienteDeleteView.as_view(), name='cliente_eliminar'),
]
    