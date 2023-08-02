from datetime import date
import datetime
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_select2 import forms as s2forms


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'


class VendedorForm(forms.ModelForm):
    class Meta:
        model = Vendedor
        fields = '__all__'


class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = '__all__'


class MonedaForm(forms.ModelForm):
    class Meta:
        model = Moneda
        fields = '__all__'


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = '__all__'


class BuForm(forms.ModelForm):
    class Meta:
        model = Bu
        fields = '__all__'


class ProformaForm(forms.ModelForm):
    class Meta:
        model = Proforma
        fields = '__all__'

    fecha = forms.DateField(
        label='Fecha O/P', widget=forms.DateInput(attrs={'type': 'date'}))

    # Añadimos los campos de correo y celular como no requeridos y ocultos
    correo = forms.EmailField(required=False, widget=forms.HiddenInput())
    celular = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Si el formulario no tiene una instancia (es decir, es para agregar una nueva proforma),
        # configuramos el valor del campo fecha en la fecha actual
        if not self.instance.pk:
            self.initial['fecha'] = date.today()

    def clean_fecha(self):
        # Si se seleccionó "Hoy", establecer la fecha actual en el campo de fecha
        fecha = self.cleaned_data['fecha']
        if fecha == date.today():
            return date.today()
        return fecha


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']
        
class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = ['proforma', 'cliente']
        widgets = {
            'proforma': forms.Select(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
        }
class PiezasRepuestoForm(forms.ModelForm):
    class Meta:
        model = piezasRepuesto
        fields = '__all__'

class descripcionWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "codigo__icontains"
    ]
    def label_from_instance(self, obj):
        return obj.codigo 
    
class DescripcionCotizacionForm(forms.ModelForm):

    class Meta:
        model = descripcionCotizacion
        fields = '__all__'
        widgets = {
            'codigo':descripcionWidget,
            'cotizacion': forms.HiddenInput(),
            'descripcion': forms.HiddenInput(),
            'precio_unitario': forms.HiddenInput(),
            # Hace que el campo Cotizacion sea oculto para el usuario
            'precio_total': forms.HiddenInput(),
            'descuento': forms.Select(attrs={'required': 'required'}),

        }

class MantenimientoForm(forms.ModelForm):
    class Meta:
        model = piezasRepuesto
        fields = '__all__'

class ConsultoriaForm(forms.ModelForm):
    class Meta:
        model = Consultoria
        fields = '__all__'

class ManoDeObraForm(forms.ModelForm):
    class Meta:
        model = ManodeObra
        fields = '__all__'
