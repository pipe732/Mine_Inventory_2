from django import forms
from Usuario.models import Usuario
from prestamos.models import Prestamo, DetallePrestamo, DevolucionHerramienta, Estado
from inventario.models import Stock


# ─────────────────────────────────────────
# FORMULARIO DE USUARIO
# ─────────────────────────────────────────
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'numero_documento',
            'id_rol',
            'nombre_completo',
            'correo',
            'telefono',
            'tipo_documento',
        ]
        widgets = {
            'numero_documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 1234567890'}),
            'id_rol':           forms.Select(attrs={'class': 'form-control'}),
            'nombre_completo':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'correo':           forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'}),
            'telefono':         forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 3001234567'}),
            'tipo_documento':   forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'numero_documento': 'Número de Documento',
            'id_rol':           'Rol',
            'nombre_completo':  'Nombre Completo',
            'correo':           'Correo Electrónico',
            'telefono':         'Teléfono',
            'tipo_documento':   'Tipo de Documento',
        }

    def clean_numero_documento(self):
        numero = self.cleaned_data.get('numero_documento')
        if not numero.isdigit():
            raise forms.ValidationError('El número de documento solo debe contener dígitos.')
        return numero

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit():
            raise forms.ValidationError('El teléfono solo debe contener dígitos.')
        return telefono

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if Usuario.objects.filter(correo=correo).exclude(
            numero_documento=self.instance.numero_documento
        ).exists():
            raise forms.ValidationError('Este correo ya está registrado.')
        return correo


# ─────────────────────────────────────────
# FORMULARIO DE PRÉSTAMO
# Conecta Usuario (numero_documento) → Prestamo
# ─────────────────────────────────────────
class PrestamoForm(forms.ModelForm):
    # Mostramos el usuario como selector legible
    numero_documento = forms.ModelChoiceField(
        queryset=Usuario.objects.all(),
        label='Usuario',
        widget=forms.Select(attrs={'class': 'form-control'}),
        to_field_name='numero_documento',
    )

    class Meta:
        model = Prestamo
        fields = ['herramienta', 'numero_documento', 'id_estado', 'observaciones']
        widgets = {
            'herramienta':    forms.Select(attrs={'class': 'form-control'}),
            'id_estado':      forms.Select(attrs={'class': 'form-control'}),
            'observaciones':  forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'herramienta':   'Herramienta',
            'id_estado':     'Estado',
            'observaciones': 'Observaciones',
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Guardamos solo el numero_documento (CharField) en el modelo
        usuario = self.cleaned_data['numero_documento']
        instance.numero_documento = usuario.numero_documento
        if commit:
            instance.save()
        return instance


# ─────────────────────────────────────────
# FORMULARIO DE DETALLE DE PRÉSTAMO
# ─────────────────────────────────────────
class DetallePrestamoForm(forms.ModelForm):
    class Meta:
        model = DetallePrestamo
        fields = ['id_prestamo', 'herramienta', 'cantidad']
        widgets = {
            'id_prestamo':  forms.Select(attrs={'class': 'form-control'}),
            'herramienta':  forms.Select(attrs={'class': 'form-control'}),
            'cantidad':     forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
        labels = {
            'id_prestamo': 'Préstamo',
            'herramienta': 'Herramienta',
            'cantidad':    'Cantidad',
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad <= 0:
            raise forms.ValidationError('La cantidad debe ser mayor a 0.')
        return cantidad


# ─────────────────────────────────────────
# FORMULARIO DE DEVOLUCIÓN
# ─────────────────────────────────────────
class DevolucionHerramientaForm(forms.ModelForm):
    class Meta:
        model = DevolucionHerramienta
        fields = ['id_detalle_prestamo', 'herramienta', 'observaciones']
        widgets = {
            'id_detalle_prestamo': forms.Select(attrs={'class': 'form-control'}),
            'herramienta':         forms.Select(attrs={'class': 'form-control'}),
            'observaciones':       forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'id_detalle_prestamo': 'Detalle de Préstamo',
            'herramienta':         'Herramienta a Devolver',
            'observaciones':       'Observaciones',
        }