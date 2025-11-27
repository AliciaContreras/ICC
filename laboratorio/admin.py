from django.contrib import admin
from .models import Cientifico, Esbirro, Invento, MaterialSospechoso, ProtocoloAutodestruccion

# Personalización del Admin
class EsbirroInline(admin.TabularInline):
    model = Esbirro
    extra = 1

@admin.register(Cientifico)
class CientificoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especialidad')
    search_fields = ('nombre',)
    inlines = [EsbirroInline] # Relación 1:N

class ProtocoloInline(admin.StackedInline):
    model = ProtocoloAutodestruccion

@admin.register(Invento)
class InventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'probabilidad_exito', 'fecha_fabricacion')
    list_filter = ('probabilidad_exito',)
    inlines = [ProtocoloInline] # Relación 1:1

admin.site.register(MaterialSospechoso)