from django import forms
from django.forms import inlineformset_factory  # <--- ESTA ERA LA LÍNEA QUE FALTABA
from .models import Invento, Cientifico, Esbirro, Receta, MaterialSospechoso

# --- 1. Formulario de Inventos ---
class InventoForm(forms.ModelForm):
    class Meta:
        model = Invento
        fields = ['nombre', 'descripcion', 'probabilidad_exito', 'fecha_fabricacion', 'foto']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del artilugio'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'probabilidad_exito': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_fabricacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# --- 2. Formulario de Científicos ---
class CientificoForm(forms.ModelForm):
    class Meta:
        model = Cientifico
        fields = ['nombre', 'especialidad', 'biografia', 'foto']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Dr. Doofenshmirtz'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Inadores'}),
            'biografia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# --- 3. Formulario de Esbirros ---
class EsbirroForm(forms.ModelForm):
    class Meta:
        model = Esbirro
        fields = ['cientifico', 'nombre', 'tiene_joroba', 'nivel_lealtad']
        widgets = {
            'cientifico': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tiene_joroba': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'nivel_lealtad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
        }

# --- 4. Formulario de Materiales Sospechosos ---
class MaterialForm(forms.ModelForm):
    class Meta:
        model = MaterialSospechoso
        fields = ['nombre', 'nivel_peligro', 'es_ilegal', 'stock_gramos']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'nivel_peligro': forms.Select(attrs={'class': 'form-select'}),
            'es_ilegal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'stock_gramos': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# --- 5. Formset para Componentes (Tabla intermedia) ---
InventoComponenteFormSet = inlineformset_factory(
    Invento,            # Padre
    Receta,             # Hijo (Intermedia)
    fields=('componente', 'cantidad'),
    extra=1,
    can_delete=True
)