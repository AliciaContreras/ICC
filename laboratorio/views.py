from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Avg
from django.contrib.auth.decorators import login_required
from django.db import transaction

# Importación de Modelos
from .models import Invento, Cientifico, Esbirro, MaterialSospechoso

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
    # 1. Consulta estándar
    inventos = Invento.objects.all().order_by('-fecha_fabricacion')

    # 2. Filter: Inventos peligrosos (éxito < 20%)
    peligrosos = Invento.objects.filter(probabilidad_exito__lt=20)

    # 3. Exclude: Inventos que NO son seguros
    inestables = Invento.objects.exclude(probabilidad_exito__gt=80)

    # 4. Annotate: Científicos líderes
    cientificos_leaders = Cientifico.objects.annotate(num_esbirros=Count('esbirros')).order_by('-num_esbirros')

    # 5. Raw SQL: Auditoría
    inventos_recientes = Invento.objects.raw('SELECT * FROM laboratorio_invento ORDER BY fecha_fabricacion DESC LIMIT 5')

    context = {
        'inventos': inventos,
        'peligrosos': peligrosos,
        'inestables': inestables,
        'cientificos': cientificos_leaders,
        'recientes_sql': inventos_recientes
    }
    return render(request, 'laboratorio/lista_inventos.html', context)

def detalle_invento(request, pk):
    invento = get_object_or_404(Invento, pk=pk)
    return render(request, 'laboratorio/detalle_invento.html', {'invento': invento})

@login_required
def crear_invento(request):
    if request.method == 'POST':
        # IMPORTANTE: request.FILES para las fotos
        form = InventoForm(request.POST, request.FILES)
        formset = InventoComponenteFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                invento = form.save()
                formset.instance = invento
                formset.save()
                
            messages.success(request, "¡Invento registrado correctamente!")
            return redirect('lista_inventos')
    else:
        form = InventoForm()
        formset = InventoComponenteFormSet()
    
    return render(request, 'laboratorio/form_invento.html', {
        'form': form, 
        'formset': formset, 
        'accion': 'Registrar'
    })

@login_required
def editar_invento(request, pk):
    invento = get_object_or_404(Invento, pk=pk)
    
    if request.method == 'POST':
        # IMPORTANTE: request.FILES y instance=invento
        form = InventoForm(request.POST, request.FILES, instance=invento)
        formset = InventoComponenteFormSet(request.POST, instance=invento)
        
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
                
            messages.info(request, "Especificaciones actualizadas.")
            return redirect('lista_inventos')
    else:
        form = InventoForm(instance=invento)
        formset = InventoComponenteFormSet(instance=invento)
    
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
        return redirect('lista_inventos')
    
    return render(request, 'laboratorio/eliminar_invento.html', {'invento': invento})

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
    if request.method == 'POST':
        # IMPORTANTE: request.FILES
        form = CientificoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Contratación exitosa!")
            return redirect('lista_cientificos')
    else:
        form = CientificoForm()
    return render(request, 'laboratorio/form_cientifico.html', {'form': form, 'accion': 'Contratar'})

@login_required
def editar_cientifico(request, pk):
    cientifico = get_object_or_404(Cientifico, pk=pk)
    if request.method == 'POST':
        # IMPORTANTE: request.FILES
        form = CientificoForm(request.POST, request.FILES, instance=cientifico)
        if form.is_valid():
            form.save()
            messages.info(request, "Datos actualizados.")
            return redirect('lista_cientificos')
    else:
        form = CientificoForm(instance=cientifico)
    return render(request, 'laboratorio/form_cientifico.html', {'form': form, 'accion': 'Actualizar'})

@login_required
def eliminar_cientifico(request, pk):
    cientifico = get_object_or_404(Cientifico, pk=pk)
    if request.method == 'POST':
        cientifico.delete()
        messages.error(request, "Personal despedido.")
        return redirect('lista_cientificos')
    return render(request, 'laboratorio/eliminar_cientifico.html', {'cientifico': cientifico})

# ========================================================
# 3. GESTIÓN DE ESBIRROS
# ========================================================

@login_required
def crear_esbirro(request, cientifico_id=None):
    initial_data = {}
    if cientifico_id:
        initial_data['cientifico'] = cientifico_id

    if request.method == 'POST':
        form = EsbirroForm(request.POST)
        if form.is_valid():
            esbirro = form.save()
            messages.success(request, "¡Esbirro reclutado!")
            return redirect('detalle_cientifico', pk=esbirro.cientifico.pk)
    else:
        form = EsbirroForm(initial=initial_data)
    
    return render(request, 'laboratorio/form_esbirro.html', {'form': form, 'accion': 'Reclutar'})

@login_required
def editar_esbirro(request, pk):
    esbirro = get_object_or_404(Esbirro, pk=pk)
    if request.method == 'POST':
        form = EsbirroForm(request.POST, instance=esbirro)
        if form.is_valid():
            esbirro = form.save()
            messages.info(request, "Esbirro modificado.")
            return redirect('detalle_cientifico', pk=esbirro.cientifico.pk)
    else:
        form = EsbirroForm(instance=esbirro)
    return render(request, 'laboratorio/form_esbirro.html', {'form': form, 'accion': 'Modificar'})

# ========================================================
# 4. GESTIÓN DE MATERIALES (BODEGA)
# ========================================================

def lista_materiales(request):
    materiales = MaterialSospechoso.objects.all().order_by('-nivel_peligro')
    return render(request, 'laboratorio/lista_materiales.html', {'materiales': materiales})

@login_required
def crear_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Material ingresado.")
            return redirect('lista_materiales')
    else:
        form = MaterialForm()
    return render(request, 'laboratorio/form_material.html', {'form': form, 'accion': 'Ingresar'})

@login_required
def editar_material(request, pk):
    material = get_object_or_404(MaterialSospechoso, pk=pk)
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            messages.info(request, "Inventario actualizado.")
            return redirect('lista_materiales')
    else:
        form = MaterialForm(instance=material)
    return render(request, 'laboratorio/form_material.html', {'form': form, 'accion': 'Actualizar'})

@login_required
def eliminar_material(request, pk):
    material = get_object_or_404(MaterialSospechoso, pk=pk)
    if request.method == 'POST':
        material.delete()
        messages.warning(request, "Material desechado.")
        return redirect('lista_materiales')
    # Reutilizamos el template de eliminar_invento, pero pasamos el objeto 'invento' como el material
    return render(request, 'laboratorio/eliminar_invento.html', {'invento': material})