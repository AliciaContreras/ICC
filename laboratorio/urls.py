from django.urls import path
from . import views

# Espacio de nombres para la app (Mejor práctica)
app_name = 'laboratorio'

urlpatterns = [
    # Dashboard / Inventos
    path('', views.lista_inventos, name='lista_inventos'),
    path('inventos/<int:pk>/', views.detalle_invento, name='detalle_invento'),
    path('inventos/crear/', views.crear_invento, name='crear_invento'),
    path('inventos/editar/<int:pk>/', views.editar_invento, name='editar_invento'),
    path('inventos/eliminar/<int:pk>/', views.eliminar_invento, name='eliminar_invento'),

    # Científicos
    path('cientificos/', views.lista_cientificos, name='lista_cientificos'),
    path('cientificos/<int:pk>/', views.detalle_cientifico, name='detalle_cientifico'),
    path('cientificos/crear/', views.crear_cientifico, name='crear_cientifico'),
    path('cientificos/editar/<int:pk>/', views.editar_cientifico, name='editar_cientifico'),
    path('cientificos/eliminar/<int:pk>/', views.eliminar_cientifico, name='eliminar_cientifico'),

    # Esbirros
    path('esbirros/crear/', views.crear_esbirro, name='crear_esbirro_general'),
    path('esbirros/crear/<int:cientifico_id>/', views.crear_esbirro, name='crear_esbirro_para_cientifico'),
    path('esbirros/editar/<int:pk>/', views.editar_esbirro, name='editar_esbirro'),
    path('esbirros/eliminar/<int:pk>/', views.eliminar_esbirro, name='eliminar_esbirro'),

    # Materiales
    path('materiales/', views.lista_materiales, name='lista_materiales'),
    path('materiales/crear/', views.crear_material, name='crear_material'),
    path('materiales/editar/<int:pk>/', views.editar_material, name='editar_material'),
    path('materiales/eliminar/<int:pk>/', views.eliminar_material, name='eliminar_material'),
]