from django.urls import path
from .views import (categoriasViews, 
    proveedoresViews, 
    productosViews, 
    facturasViews,
    vendedoresViews,
    transportadoresViews,
    )

urlpatterns = [
    path('proveedores/', proveedoresViews.VerProveedores, name="verProveedores"),
    path('nuevoProveedor/', proveedoresViews.CrearProveedores, name="crearProveedor"),
    path('editarProveedor/<str:pk>', proveedoresViews.EditarProveedor, name="editarProveedor"),
    path('eliminarProveedor/<str:pk>', proveedoresViews.EliminarProveedor, name="eliminarProveedor"),

    path('productos/', productosViews.VerProductos, name="verProductos"),
    path('nuevoProducto/', productosViews.CrearProducto, name="CrearProducto"),
    path('editarProducto/<str:pk>', productosViews.EditarProducto, name="editarProducto"),
    path('eliminarProducto/<str:pk>', productosViews.EliminarProducto, name="eliminarProducto"),

    path('categorias/', categoriasViews.VerCategorias, name="VerCategorias"),
    path('nuevaCategoria/', categoriasViews.CrearCategoria, name="CrearCategoria"),
    path('editarCategoria/<str:pk>', categoriasViews.EditarCategoria, name="EditarCategoria"),
    path('eliminarCategoria/<str:pk>', categoriasViews.EliminarCategoria, name="EliminarCategoria"),

    path('facturas/', facturasViews.VerFacturas, name="VerFacturas"),
    path('nuevaFactura/', facturasViews.CrearFactura, name="CrearFactura"),
    path('editarFactura/<str:pk>', facturasViews.EditarFactura, name="EditarFactura"),
    path('eliminarFactura/<str:pk>', facturasViews.EliminarFactura, name="EliminarFactura"),

    path('vendedores/', vendedoresViews.VerVendedores, name="VerVendedores"),
    path('nuevoVendedor/', vendedoresViews.CrearVendedor, name="CrearVendedores"),
    path('editarVendedor/<str:pk>', vendedoresViews.EditarVendedor, name="EditarVendedores"),
    path('eliminarVendedor/<str:pk>', vendedoresViews.EliminarVendedor, name="EliminarVendedores"),

    path('transportadores/', transportadoresViews.VerTransportadores, name="Vertransportadores"),
    path('nuevoTransportador/', transportadoresViews.CrearTransportador, name="Creartransportador"),
    path('editarTransportador/<str:pk>', transportadoresViews.EditarTransportador, name="Editartransportador"),
    path('eliminarTransportador/<str:pk>', transportadoresViews.EliminarTransportador, name="Eliminartransportador"),
]