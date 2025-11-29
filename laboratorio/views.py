import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.db import transaction

# Importación de Modelos
from .models import Invento, Cientifico, Esbirro, MaterialSospechoso, Componente

# Importación de Formularios
from .forms import (
    InventoForm, 
    CientificoForm, 
    EsbirroForm, 
    InventoComponenteFormSet, 
    MaterialForm
)

# ========================================================
# 1. GESTIÓN DE INVENTOS (Dashboard Principal)
# ========================================================

def lista_inventos(request):
    inventos = Invento.objects.prefetch_related('componentes').all().order_by('-fecha_fabricacion')
    peligrosos = Invento.objects.filter(probabilidad_exito__lt=20)
    inestables = Invento.objects.exclude(probabilidad_exito__gt=80)
    cientificos_leaders = Cientifico.objects.annotate(num_esbirros=Count('esbirros')).order_by('-num_esbirros')
    inventos_recientes = Invento.objects.all().order_by('-fecha_fabricacion')[:5]

    # --- NUEVA LÓGICA PARA EL SIMULADOR ---
    # Obtener nombres reales de la BD
    lista_componentes = list(Componente.objects.values_list('nombre', flat=True))
    lista_materiales = list(MaterialSospechoso.objects.values_list('nombre', flat=True))
    
    # Crear una lista mixta para pasarsela al JS
    datos_simulador = []
    for c in lista_componentes:
        datos_simulador.append({'nombre': c, 'tipo': 'componente'})
    for m in lista_materiales:
        datos_simulador.append({'nombre': m, 'tipo': 'material'})
    
    # Convertir a JSON string para que JS lo lea sin problemas
    datos_simulador_json = json.dumps(datos_simulador)

    context = {
        'inventos': inventos,
        'peligrosos': peligrosos,
        'inestables': inestables,
        'cientificos': cientificos_leaders,
        'recientes_sql': inventos_recientes,
        'datos_simulador': datos_simulador_json # <--- PASAR EL JSON
    }
    return render(request, 'laboratorio/lista_inventos.html', context)

def detalle_invento(request, pk):
    invento = get_object_or_404(Invento, pk=pk)
    return render(request, 'laboratorio/detalle_invento.html', {'invento': invento})

@login_required
def crear_invento(request):
    if request.method != 'POST':
        return render(request, 'laboratorio/form_invento.html', {
            'form': InventoForm(),
            'formset': InventoComponenteFormSet(),
            'accion': 'Registrar',
            'titulo': 'Nuevo Invento'
        })

    form = InventoForm(request.POST, request.FILES)
    formset = InventoComponenteFormSet(request.POST)
    
    if not (form.is_valid() and formset.is_valid()):
        messages.error(request, "Error en el formulario. Revisa los datos.")
        return render(request, 'laboratorio/form_invento.html', {
            'form': form,
            'formset': formset,
            'accion': 'Registrar',
            'titulo': 'Nuevo Invento'
        })

    with transaction.atomic():
        invento = form.save()
        formset.instance = invento
        formset.save()
        
    messages.success(request, "¡Invento registrado correctamente!")
    # CORREGIDO: namespace
    return redirect('laboratorio:lista_inventos')

@login_required
def editar_invento(request, pk):
    invento = get_object_or_404(Invento, pk=pk)
    
    if request.method != 'POST':
        return render(request, 'laboratorio/form_invento.html', {
            'form': InventoForm(instance=invento),
            'formset': InventoComponenteFormSet(instance=invento),
            'accion': 'Actualizar',
            'titulo': f'Editando: {invento.nombre}'
        })

    form = InventoForm(request.POST, request.FILES, instance=invento)
    formset = InventoComponenteFormSet(request.POST, instance=invento)
    
    if form.is_valid() and formset.is_valid():
        with transaction.atomic():
            form.save()
            formset.save()
        messages.info(request, "Especificaciones actualizadas.")
        # CORREGIDO: namespace
        return redirect('laboratorio:lista_inventos')
        
    messages.error(request, "No se pudo actualizar el invento.")
    return render(request, 'laboratorio/form_invento.html', {
        'form': form, 
        'formset': formset, 
        'accion': 'Actualizar'
    })

@login_required
def eliminar_invento(request, pk):
    invento = get_object_or_404(Invento, pk=pk)
    if request.method == 'POST':
        invento.delete()
        messages.warning(request, "Invento destruido.")
        # CORREGIDO: namespace
        return redirect('laboratorio:lista_inventos')
    
    return render(request, 'laboratorio/eliminar_invento.html', {
        'objeto': invento, 
        'tipo_objeto': 'Invento' 
    })

# ========================================================
# 2. GESTIÓN DE CIENTÍFICOS
# ========================================================

def lista_cientificos(request):
    cientificos = Cientifico.objects.annotate(total_esbirros=Count('esbirros')).order_by('nombre')
    return render(request, 'laboratorio/lista_cientificos.html', {'cientificos': cientificos})

def detalle_cientifico(request, pk):
    cientifico = get_object_or_404(Cientifico, pk=pk)
    esbirros = cientifico.esbirros.all() 
    
    return render(request, 'laboratorio/detalle_cientifico.html', {
        'cientifico': cientifico,
        'esbirros': esbirros
    })

@login_required
def crear_cientifico(request):
    if request.method != 'POST':
        return render(request, 'laboratorio/form_cientifico.html', {
            'form': CientificoForm(), 
            'accion': 'Contratar'
        })

    form = CientificoForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        messages.success(request, "¡Contratación exitosa!")
        # CORREGIDO: namespace
        return redirect('laboratorio:lista_cientificos')
    
    return render(request, 'laboratorio/form_cientifico.html', {'form': form, 'accion': 'Contratar'})

@login_required
def editar_cientifico(request, pk):
    cientifico = get_object_or_404(Cientifico, pk=pk)
    
    if request.method != 'POST':
         return render(request, 'laboratorio/form_cientifico.html', {
             'form': CientificoForm(instance=cientifico), 
             'accion': 'Actualizar'
         })

    form = CientificoForm(request.POST, request.FILES, instance=cientifico)
    if form.is_valid():
        form.save()
        messages.info(request, "Datos actualizados.")
        # CORREGIDO: namespace
        return redirect('laboratorio:lista_cientificos')
    
    return render(request, 'laboratorio/form_cientifico.html', {'form': form, 'accion': 'Actualizar'})

@login_required
def eliminar_cientifico(request, pk):
    cientifico = get_object_or_404(Cientifico, pk=pk)
    if request.method == 'POST':
        cientifico.delete()
        messages.error(request, "Personal despedido.")
        # CORREGIDO: namespace
        return redirect('laboratorio:lista_cientificos')
    return render(request, 'laboratorio/eliminar_cientifico.html', {'cientifico': cientifico})

# ========================================================
# 3. GESTIÓN DE ESBIRROS
# ========================================================

@login_required
def crear_esbirro(request, cientifico_id=None):
    initial_data = {}
    if cientifico_id:
        initial_data['cientifico'] = cientifico_id

    if request.method != 'POST':
        return render(request, 'laboratorio/form_esbirro.html', {
            'form': EsbirroForm(initial=initial_data), 
            'accion': 'Reclutar'
        })

    form = EsbirroForm(request.POST)
    if form.is_valid():
        esbirro = form.save()
        messages.success(request, "¡Esbirro reclutado!")
        # CORREGIDO: namespace
        return redirect('laboratorio:detalle_cientifico', pk=esbirro.cientifico.pk)

    return render(request, 'laboratorio/form_esbirro.html', {'form': form, 'accion': 'Reclutar'})

@login_required
def editar_esbirro(request, pk):
    esbirro = get_object_or_404(Esbirro, pk=pk)
    
    if request.method != 'POST':
        return render(request, 'laboratorio/form_esbirro.html', {
            'form': EsbirroForm(instance=esbirro), 
            'accion': 'Modificar'
        })

    form = EsbirroForm(request.POST, instance=esbirro)
    if form.is_valid():
        esbirro = form.save()
        messages.info(request, "Esbirro modificado.")
        # CORREGIDO: namespace
        return redirect('laboratorio:detalle_cientifico', pk=esbirro.cientifico.pk)
        
    return render(request, 'laboratorio/form_esbirro.html', {'form': form, 'accion': 'Modificar'})


@login_required
def eliminar_esbirro(request, pk):
    esbirro = get_object_or_404(Esbirro, pk=pk)
    # Guardamos el ID del jefe para volver a su perfil después de borrar al esbirro
    cientifico_id = esbirro.cientifico.id
    
    if request.method == 'POST':
        esbirro.delete()
        messages.warning(request, "Esbirro dado de baja.")
        return redirect('laboratorio:detalle_cientifico', pk=cientifico_id)
    
    # Reutilizamos la plantilla genérica de eliminación que ya creamos
    return render(request, 'laboratorio/eliminar_invento.html', {
        'objeto': esbirro, 
        'tipo_objeto': 'Esbirro' 
    })

# ========================================================
# 4. GESTIÓN DE MATERIALES (BODEGA)
# ========================================================

def lista_materiales(request):
    materiales = MaterialSospechoso.objects.all().order_by('-nivel_peligro')
    return render(request, 'laboratorio/lista_materiales.html', {'materiales': materiales})

@login_required
def crear_material(request):
    if request.method != 'POST':
         return render(request, 'laboratorio/form_material.html', {
             'form': MaterialForm(), 
             'accion': 'Ingresar'
         })

    form = MaterialForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Material ingresado.")
        # CORREGIDO: namespace
        return redirect('laboratorio:lista_materiales')

    return render(request, 'laboratorio/form_material.html', {'form': form, 'accion': 'Ingresar'})

@login_required
def editar_material(request, pk):
    material = get_object_or_404(MaterialSospechoso, pk=pk)
    
    if request.method != 'POST':
        return render(request, 'laboratorio/form_material.html', {
            'form': MaterialForm(instance=material), 
            'accion': 'Actualizar'
        })
        
    form = MaterialForm(request.POST, instance=material)
    if form.is_valid():
        form.save()
        messages.info(request, "Inventario actualizado.")
        # CORREGIDO: namespace
        return redirect('laboratorio:lista_materiales')

    return render(request, 'laboratorio/form_material.html', {'form': form, 'accion': 'Actualizar'})

@login_required
def eliminar_material(request, pk):
    material = get_object_or_404(MaterialSospechoso, pk=pk)
    if request.method == 'POST':
        material.delete()
        messages.warning(request, "Material desechado.")
        # CORREGIDO: namespace
        return redirect('laboratorio:lista_materiales')
    
    return render(request, 'laboratorio/eliminar_invento.html', {
        'objeto': material, 
        'tipo_objeto': 'Material Sospechoso' 
    })