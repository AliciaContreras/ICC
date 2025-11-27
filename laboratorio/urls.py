from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_inventos, name='lista_inventos'),
    path('crear/', views.crear_invento, name='crear_invento'),
    path('editar/<int:pk>/', views.editar_invento, name='editar_invento'),
    path('eliminar/<int:pk>/', views.eliminar_invento, name='eliminar_invento'),
    path('cientificos/', views.lista_cientificos, name='lista_cientificos'),
    path('cientificos/<int:pk>/', views.detalle_cientifico, name='detalle_cientifico'),
    path('inventos/<int:pk>/', views.detalle_invento, name='detalle_invento'),
    path('cientificos/crear/', views.crear_cientifico, name='crear_cientifico'),
    path('cientificos/editar/<int:pk>/', views.editar_cientifico, name='editar_cientifico'),
    path('cientificos/eliminar/<int:pk>/', views.eliminar_cientifico, name='eliminar_cientifico'),
    path('esbirros/crear/', views.crear_esbirro, name='crear_esbirro_general'),
    path('esbirros/crear/<int:cientifico_id>/', views.crear_esbirro, name='crear_esbirro_para_cientifico'),
    path('esbirros/editar/<int:pk>/', views.editar_esbirro, name='editar_esbirro'),
    path('materiales/', views.lista_materiales, name='lista_materiales'),
    path('materiales/crear/', views.crear_material, name='crear_material'),
    path('materiales/editar/<int:pk>/', views.editar_material, name='editar_material'),
    path('materiales/eliminar/<int:pk>/', views.eliminar_material, name='eliminar_material'),
]