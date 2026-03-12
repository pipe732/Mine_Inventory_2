from django import forms
from .models import Stock, CategoriaHerramienta

class StockForm(forms.ModelForm):
    class Meta:
        model  = Stock
        fields = ['codigo', 'herramienta', 'categoria', 'ubicacion', 'estado', 'observaciones', 'proveedor']  # ← NUEVO
        widgets = {
            'codigo':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: HRR-001'}),
            'herramienta':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Martillo neumático'}),
            'categoria':    forms.Select(attrs={'class': 'form-select'}),
            'ubicacion':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Nivel 3 – Galería B'}),
            'proveedor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Ferretería XYZ'}),
            'estado':       forms.Select(attrs={'class': 'form-select'}),
            'observaciones':forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }