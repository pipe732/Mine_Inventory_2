from django import forms
from .models import BitacoraEstado, BitacoraMantenimiento, DetalleMantenimiento

class DetalleMantenimientoForm(forms.ModelForm):
    class Meta:
        model = DetalleMantenimiento

        fields = ['motivo_mantenimiento', 'descripcion'] 
        widgets = {
            'motivo_mantenimiento': forms.TextInput(attrs={'class': 'form-control bg-dark text-cream'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control bg-dark text-cream'}),
        }
class BitacoraEstadoForm(forms.ModelForm):
    class Meta:
        model = BitacoraEstado
        fields = ['descripcion', 'estado', 'nivel_estado']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control bg-dark text-cream'}),
            'estado': forms.Select(attrs={'class': 'form-select bg-dark text-cream'}),
            'nivel_estado': forms.NumberInput(attrs={'class': 'form-control bg-dark text-cream'}),
        }

class BitacoraMantenimientoForm(forms.ModelForm):
    class Meta:
        model = BitacoraMantenimiento
        fields = ['id_bitacora_estado', 'tipo_mantenimiento']
        widgets = {
            'id_bitacora_estado': forms.Select(attrs={'class': 'form-select bg-dark text-cream'}),
            'tipo_mantenimiento': forms.Select(attrs={'class': 'form-select bg-dark text-cream'}),
        }