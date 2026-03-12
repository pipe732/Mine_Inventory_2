from django import forms
from django.forms import inlineformset_factory

from inventario.models import Stock
from .models import (
    Prestamo,
    DetallePrestamo,
    DevolucionHerramienta,
    Estado,
)


# ─────────────────────────────────────────────
# Widget helpers
# ─────────────────────────────────────────────

class StockSelect(forms.Select):
    """Dropdown que muestra código + nombre de herramienta."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.setdefault('class', 'form-select')


# ─────────────────────────────────────────────
# Préstamo
# ─────────────────────────────────────────────

class PrestamoForm(forms.ModelForm):
    """Formulario principal de préstamo."""

    numero_documento = forms.ModelChoiceField(
        queryset=Usuario.objects.all(),
        label='Usuario (documento)',
        widget=forms.Select(attrs={'class': 'form-select'}),
        to_field_name='numero_documento',
    )

    id_estado = forms.ModelChoiceField(
        queryset=Estado.objects.all(),
        label='Estado',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    observaciones = forms.CharField(
        label='Observaciones',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Observaciones opcionales…',
        }),
    )

    class Meta:
        model = Prestamo
        fields = ['numero_documento', 'id_estado', 'observaciones']


# ─────────────────────────────────────────────
# Detalle de Préstamo
# ─────────────────────────────────────────────

class DetallePrestamoForm(forms.ModelForm):
    """
    Línea individual de herramienta dentro de un préstamo.
    Solo muestra herramientas con estado 'disponible'.
    """

    herramienta = forms.ModelChoiceField(
        queryset=Stock.objects.filter(estado='disponible'),
        label='Herramienta',
        widget=StockSelect(),
    )

    cantidad = forms.IntegerField(
        label='Cantidad',
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1,
        }),
    )

    class Meta:
        model = DetallePrestamo
        fields = ['herramienta', 'cantidad']

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad < 1:
            raise forms.ValidationError('La cantidad debe ser al menos 1.')
        return cantidad


# FormSet: múltiples detalles ligados a un Préstamo
DetallePrestamoFormSet = inlineformset_factory(
    Prestamo,
    DetallePrestamo,
    form=DetallePrestamoForm,
    extra=1,          # 1 línea vacía por defecto
    can_delete=True,  # permite eliminar filas existentes
    min_num=1,        # al menos 1 herramienta
    validate_min=True,
)


# ─────────────────────────────────────────────
# Devolución de Herramienta
# ─────────────────────────────────────────────

class DevolucionHerramientaForm(forms.ModelForm):
    """Registra la devolución de una herramienta prestada."""

    id_detalle_prestamo = forms.ModelChoiceField(
        queryset=DetallePrestamo.objects.select_related(
            'id_prestamo', 'herramienta'
        ),
        label='Detalle de préstamo',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    herramienta = forms.ModelChoiceField(
        queryset=Stock.objects.all(),
        label='Herramienta devuelta',
        widget=StockSelect(),
    )

    observaciones = forms.CharField(
        label='Observaciones',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Estado de la herramienta al devolver…',
        }),
    )

    class Meta:
        model = DevolucionHerramienta
        fields = ['id_detalle_prestamo', 'herramienta', 'observaciones']

    def clean(self):
        cleaned_data = super().clean()
        detalle = cleaned_data.get('id_detalle_prestamo')
        herramienta = cleaned_data.get('herramienta')

        # Validar que la herramienta devuelta coincide con el detalle
        if detalle and herramienta:
            if detalle.herramienta != herramienta:
                raise forms.ValidationError(
                    'La herramienta devuelta no coincide con el detalle del préstamo.'
                )
        return cleaned_data



# ─────────────────────────────────────────────
# Búsqueda / Filtros (no ligados a modelos)
# ─────────────────────────────────────────────

class FiltroPrestamosForm(forms.Form):
    """Filtros para listar préstamos."""

    usuario = forms.CharField(
        label='Documento / nombre',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar usuario…',
        }),
    )

    estado = forms.ModelChoiceField(
        queryset=Estado.objects.all(),
        label='Estado',
        required=False,
        empty_label='Todos',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    herramienta = forms.ModelChoiceField(
        queryset=Stock.objects.all(),
        label='Herramienta',
        required=False,
        empty_label='Todas',
        widget=StockSelect(),
    )