from django.contrib import admin
from django.urls import path
from . import views

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),

    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),

    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    
    path('',views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('cliente/', views.ClienteView.as_view(), name='cliente'),
    path('cliente/nuevo/', views.ClienteAgregarView.as_view(), name='nuevo_cliente'),
    path('cliente/editar/<int:pk>/', views.ClienteEditarView.as_view(), name='editar_cliente'),
    path('clientes/eliminar/<int:pk>/', views.ClienteEliminarView.as_view(), name='eliminar_cliente'),
    path('vendedor/', views.VendedorView.as_view(), name='vendedor'),
    path('vendedor/agregar/', views.VendedorAgregarView.as_view(), name='agregar_vendedor'),
    path('vendedor/editar/<int:pk>/', views.VendedorEditarView.as_view(), name='editar_vendedor'),
    path('vendedor/eliminar/<int:pk>/', views.VendedorEliminarView.as_view(), name='eliminar_vendedor'),
    path('proformas/', views.ProformaView.as_view(), name='proforma'),
    path('proformas/agregar/', views.ProformaAgregarView.as_view(), name='agregar_proforma'),
    path('proformas/editar/<int:pk>/', views.ProformaEditarView.as_view(), name='editar_proforma'),
    path('proformas/eliminar/<int:pk>/', views.ProformaEliminarView.as_view(), name='eliminar_proforma'),
    path('get_vendedor_data/<int:vendedor_id>/', views.get_vendedor_data, name='get_vendedor_data'),
    path('proformas/duplicar/<int:proforma_id>/', views.duplicar_proforma, name='duplicar_proforma'),
    path('cotizacion/agregar/', views.CotizacionAgregarView.as_view(), name='agregar_cotizacion'),
    path('cotizacion/', views.CotizacionView.as_view(), name='cotizacion'),
    path('cotizacion/editar/<int:pk>/', views.CotizacionEditarView.as_view(), name='editar_cotizacion'),
    path('cotizacion/eliminar/<int:pk>/', views.CotizacionEliminarView.as_view(), name='eliminar_cotizacion'),
    path('cotizacion/<int:pk>/detalle/', views.detalle_cotizacion, name='detalle_cotizacion'),
    path('cotizacion/<int:pk>/detalle/<int:detalle_id>/', views.detalle_cotizacion, name='editar_detalle'),
    path('cotizacion/eliminar_detalle/<int:pk>/', views.DetalleEliminarView.as_view(), name='eliminar_detalle'),
    path('cotizacion/generar_pdf/<int:pk>/', views.generar_pdf, name='generar_pdf'),

    path('cambio/', views.cambio, name='cambio'),








]