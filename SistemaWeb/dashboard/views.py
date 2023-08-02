

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from xhtml2pdf import pisa
from .forms import *
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordResetView
from .models import *
from django.contrib.auth.decorators import login_required
import requests
from django.template.loader import render_to_string
import json

from decimal import Decimal
from django.utils.text import slugify


# Create your views here


@login_required
def inicio(request):
    return render(request, 'principal.html')


def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(
                username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            return redirect(to='inicio')

        data["form"] = formulario
    return render(request, 'registration/registro.html', data)


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'

# -------CLIENTE--------


class ClienteView(View):
    def get(self, request):
        listaClientes = Cliente.objects.all()
        formCliente = ClienteForm()
        direcciones = Direccion.objects.all()

        direcciones_por_cliente = {}  # Crear el diccionario aquí

        for direccion in direcciones:
            if direccion.cliente.id not in direcciones_por_cliente:
                direcciones_por_cliente[direccion.cliente.id] = []
            direcciones_por_cliente[direccion.cliente.id].append(direccion)

        context = {
            'clientes': listaClientes,
            'formClientes': formCliente,
            'direcciones_por_cliente': direcciones_por_cliente,
        }
        return render(request, 'clientes.html', context)


class ClienteAgregarView(View):

    def get(self, request):
        formCliente = ClienteForm()
        context = {
            'formCliente': formCliente,
        }
        return render(request, 'agregarCliente.html', context)

    def post(self, request):
        formCliente = ClienteForm(request.POST)
        if formCliente.is_valid():
            formCliente.save()
            # Redirige a la lista de clientes después de guardar correctamente
            return redirect('cliente')

        context = {
            'formCliente': formCliente,
        }
        return render(request, 'agregarCliente.html', context)


class ClienteEditarView(View):

    def get(self, request, pk):
        cliente = get_object_or_404(Cliente, pk=pk)
        formCliente = ClienteForm(instance=cliente)
        context = {
            'formCliente': formCliente,
        }
        return render(request, 'agregarCliente.html', context)

    def post(self, request, pk):
        cliente = get_object_or_404(Cliente, pk=pk)
        formCliente = ClienteForm(request.POST, instance=cliente)
        if formCliente.is_valid():
            formCliente.save()
            # Redirige a la lista de clientes después de guardar correctamente
            return redirect('cliente')

        context = {
            'formCliente': formCliente,
        }
        return render(request, 'agregarCliente.html', context)


class ClienteEliminarView(View):

    def post(self, request, pk):
        cliente = get_object_or_404(Cliente, pk=pk)
        cliente.delete()
        return JsonResponse({'message': 'Cliente eliminado correctamente'})

# ---------FIN CLIENTE---------------------------


class VendedorView(View):

    def get(self, request):
        listaVendedores = Vendedor.objects.all()
        formVendedor = VendedorForm()
        context = {
            'vendedores': listaVendedores,
            'formVendedores': formVendedor
        }
        return render(request, 'vendedor.html', context)


class VendedorAgregarView(View):

    def get(self, request):
        formVendedor = VendedorForm()

        context = {
            'formVendedor': formVendedor,
        }
        return render(request, 'agregar_vendedor.html', context)

    def post(self, request):
        formVendedor = VendedorForm(request.POST)
        if formVendedor.is_valid():
            # Realizar validación personalizada si es necesario
            formVendedor.save()
            # Redireccionar a la misma página de agregar vendedor después de guardar correctamente
            return redirect('vendedor')

        # Si el formulario no es válido o hubo algún error, renderizar el template con el formulario y los errores
        context = {
            'formVendedor': formVendedor,
        }
        return render(request, 'agregar_vendedor.html', context)


class VendedorEditarView(View):

    def get(self, request, pk):
        vendedor = get_object_or_404(Vendedor, pk=pk)
        formVendedor = VendedorForm(instance=vendedor)
        context = {
            'formVendedor': formVendedor,
        }
        return render(request, 'agregar_vendedor.html', context)

    def post(self, request, pk):
        vendedor = get_object_or_404(Vendedor, pk=pk)
        formVendedor = VendedorForm(request.POST, instance=vendedor)
        if formVendedor.is_valid():
            formVendedor.save()
            # Redirige a la lista de vendedores después de guardar correctamente
            return redirect('vendedor')

        context = {
            'formVendedor': formVendedor,
        }
        return render(request, 'agregar_vendedor.html', context)


class VendedorEliminarView(View):

    def post(self, request, pk):
        vendedor = get_object_or_404(Vendedor, pk=pk)
        vendedor.delete()
        return JsonResponse({'message': 'Vendedor eliminado correctamente'})
# ---------FIN Vendedor---------------------------


class ProformaView(View):

    def get(self, request):
        listaProformas = Proforma.objects.all()
        context = {
            'proformas': listaProformas
        }
        return render(request, 'proforma.html', context)


class ProformaAgregarView(View):

    def get(self, request):
        # Obtener las listas de objetos para cada modelo
        lista_bu = Bu.objects.all()
        lista_pago = Pago.objects.all()
        lista_moneda = Moneda.objects.all()
        lista_vendedor = Vendedor.objects.all()

        # Crear el formulario y ocultar los campos de "correo" y "celular"
        formProforma = ProformaForm()
        formProforma.fields['correo'].widget.attrs['hidden'] = True
        formProforma.fields['celular'].widget.attrs['hidden'] = True

        context = {
            'formProforma': formProforma,
            'lista_bu': lista_bu,
            'lista_pago': lista_pago,
            'lista_moneda': lista_moneda,
            'lista_vendedor': lista_vendedor,
        }
        return render(request, 'agregar_proforma.html', context)

    def post(self, request):
        formProforma = ProformaForm(request.POST)
        if formProforma.is_valid():
            formProforma.save()
            return redirect('proforma')

        # Si el formulario no es válido, volvemos a mostrarlo con los errores
        lista_bu = Bu.objects.all()
        lista_pago = Pago.objects.all()
        lista_moneda = Moneda.objects.all()
        lista_vendedor = Vendedor.objects.all()

        # Ocultar los campos de "correo" y "celular"
        formProforma.fields['correo'].widget.attrs['hidden'] = True
        formProforma.fields['celular'].widget.attrs['hidden'] = True

        context = {
            'formProforma': formProforma,
            'lista_bu': lista_bu,
            'lista_pago': lista_pago,
            'lista_moneda': lista_moneda,
            'lista_vendedor': lista_vendedor,
        }
        return render(request, 'agregar_proforma.html', context)


class ProformaEditarView(View):

    def get(self, request, pk):
        proforma = get_object_or_404(Proforma, pk=pk)
        formProforma = ProformaForm(instance=proforma)

        # Obtener las listas de objetos para cada modelo
        lista_bu = Bu.objects.all()
        lista_pago = Pago.objects.all()
        lista_moneda = Moneda.objects.all()
        lista_vendedor = Vendedor.objects.all()

        context = {
            'formProforma': formProforma,
            'proforma': proforma,
            'lista_bu': lista_bu,
            'lista_pago': lista_pago,
            'lista_moneda': lista_moneda,
            'lista_vendedor': lista_vendedor,
        }

        return render(request, 'agregar_proforma.html', context)

    def post(self, request, pk):
        proforma = get_object_or_404(Proforma, pk=pk)
        formProforma = ProformaForm(request.POST, instance=proforma)

        if formProforma.is_valid():
            formProforma.save()
            return redirect('proforma')

        # Si el formulario no es válido, volvemos a mostrarlo con los errores
        lista_bu = Bu.objects.all()
        lista_pago = Pago.objects.all()
        lista_moneda = Moneda.objects.all()
        lista_vendedor = Vendedor.objects.all()

        context = {
            'formProforma': formProforma,
            'proforma': proforma,
            'lista_bu': lista_bu,
            'lista_pago': lista_pago,
            'lista_moneda': lista_moneda,
            'lista_vendedor': lista_vendedor,
        }

        return render(request, 'agregar_proforma.html', context)


class ProformaEliminarView(View):

    def post(self, request, pk):
        proforma = get_object_or_404(Proforma, pk=pk)
        proforma.delete()
        return JsonResponse({'message': 'Proforma eliminada correctamente'})


def get_vendedor_data(request, vendedor_id):
    try:
        vendedor = Vendedor.objects.get(pk=vendedor_id)
        data = {
            'correo': vendedor.correo,
            'celular': vendedor.celular,
        }
        return JsonResponse(data)
    except Vendedor.DoesNotExist:
        return JsonResponse({'error': 'Vendedor no encontrado'}, status=404)


def duplicar_proforma(request, proforma_id):
    original_proforma = Proforma.objects.get(pk=proforma_id)
    nueva_proforma = original_proforma
    nueva_proforma.pk = None  # Asignar None para crear una nueva proforma
    nueva_proforma.save()
    return redirect('proforma')  # Redirigir a la página de todas las proformas


class CotizacionView(View):

    def get(self, request):
        listaCotizaciones = Cotizacion.objects.all()
        context = {
            'cotizaciones': listaCotizaciones
        }
        return render(request, 'cotizacion.html', context)


class CotizacionAgregarView(View):

    def get(self, request):
        # Obtener las listas de objetos para cada modelo (puedes personalizar esto según tus necesidades)
        lista_proformas = Proforma.objects.all()
        lista_clientes = Cliente.objects.all()

        # Crear una instancia del formulario de cotización
        form_cotizacion = CotizacionForm()

        context = {
            # Agregar esta línea para pasar la variable cotizacion al contexto
            'formCotizacion': form_cotizacion,
            'lista_proformas': lista_proformas,
            'lista_clientes': lista_clientes
        }

        return render(request, 'agregar_cotizacion.html', context)

    def post(self, request):
        # Obtener las listas de objetos para cada modelo (puedes personalizar esto según tus necesidades)
        lista_proformas = Proforma.objects.all()
        lista_clientes = Cliente.objects.all()

        # Crear una instancia del formulario de cotización con los datos enviados por el usuario
        form_cotizacion = CotizacionForm(request.POST)

        if form_cotizacion.is_valid():
            form_cotizacion.save()
            # Redirige a la lista de cotizaciones después de guardar correctamente
            return redirect('cotizacion')

        context = {
            'form_cotizacion': form_cotizacion,
            'lista_proformas': lista_proformas,
            'lista_clientes': lista_clientes,
        }

        return render(request, 'agregar_cotizacion.html', context)


class CotizacionEditarView(View):

    def get(self, request, pk):
        cotizacion = get_object_or_404(Cotizacion, pk=pk)
        form_cotizacion = CotizacionForm(instance=cotizacion)

        # Obtener las listas de objetos para cada modelo
        lista_proformas = Proforma.objects.all()
        lista_clientes = Cliente.objects.all()

        context = {
            'form_Cotizacion': form_cotizacion,
            'cotizacion': cotizacion,
            'lista_proformas': lista_proformas,
            'lista_clientes': lista_clientes
        }

        return render(request, 'agregar_cotizacion.html', context)

    def post(self, request, pk):
        cotizacion = get_object_or_404(Cotizacion, pk=pk)
        form_cotizacion = CotizacionForm(request.POST, instance=cotizacion)

        if form_cotizacion.is_valid():
            form_cotizacion.save()
            return redirect('cotizacion')

        # Si el formulario no es válido, volvemos a mostrarlo con los errores
        lista_proformas = Proforma.objects.all()
        lista_clientes = Cliente.objects.all()

        context = {
            'form_cotizacion': form_cotizacion,
            'cotizacion': cotizacion,
            'lista_proformas': lista_proformas,
            'lista_clientes': lista_clientes
        }

        return render(request, 'agregar_cotizacion.html', context)


class CotizacionEliminarView(View):

    def post(self, request, pk):
        cotizacion = get_object_or_404(Cotizacion, pk=pk)
        cotizacion.delete()
        return JsonResponse({'message': 'Cotizacion eliminada correctamente'})


def detalle_cotizacion(request, pk, detalle_id=None):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    detalles = descripcionCotizacion.objects.filter(cotizacion=cotizacion)

    # Si se proporciona un detalle_id, es una solicitud de edición
    if detalle_id:
        detalle = get_object_or_404(descripcionCotizacion, pk=detalle_id)
    else:
        detalle = None
    
    url = "https://openexchangerates.org/api/latest.json?app_id=7d48f3c6338b4e96838cf8d894162b40&symbols=PEN,USD"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            rates = data["rates"]
            pen_rate = rates.get("PEN")
            usd_rate = rates.get("USD")
        else:
            pen_rate = None
            usd_rate = None
    except requests.exceptions.RequestException as e:
        # Si hay un error en la solicitud, puedes manejarlo aquí
        pen_rate = None
        usd_rate = None
    # Procesar el formulario de conversión a dólares
    
    if request.method == 'POST' and 'conversion-form' in request.POST:
        pen_rate = request.POST.get('pen_rate')
        if pen_rate:
            pen_rate = Decimal(pen_rate)
            for detalle in detalles:
                detalle.precio_unitario = round(detalle.precio_unitario / pen_rate, 2)
                detalle.save()

    if request.method == 'POST':
        # Si es una edición, instanciamos el formulario con el detalle existente
        # Si es una adición, instanciamos el formulario sin datos vinculados
        form = DescripcionCotizacionForm(request.POST, instance=detalle)
        if form.is_valid():
            nuevo_detalle = form.save(commit=False)
            nuevo_detalle.cotizacion = cotizacion  # Asignar la cotización al nuevo detalle
            if cotizacion.proforma.moneda.tipo == 'DOLARES':
                nuevo_detalle.precio_unitario /= Decimal(pen_rate)
            nuevo_detalle.save()
            # Imprime el nuevo detalle para verificar si está bien guardado
            print("Nuevo detalle guardado:", nuevo_detalle)
            return redirect('detalle_cotizacion', pk=pk)
        else:
            # Imprime los errores del formulario en la consola
            print("Formulario inválido:", form.errors)
    else:
        # Si no hay detalle existente, muestra el formulario vacío
        form = DescripcionCotizacionForm(
            initial={'cotizacion': cotizacion}, instance=detalle)

    # ---------------CAMBIO DOLAR-----------------------------
    # Procesar el formulario de conversión a dólares

    

    context = {
        'cotizacion': cotizacion,
        'detalles': detalles,
        'form': form,
        'pen_rate': pen_rate,
        'usd_rate': usd_rate
    }
    return render(request, 'detalle_cotizacion.html', context)
# ------------FIN COTIZACION-------------------


def cambio(request):
    # URL de la API que proporciona las tasas de cambio
    url = "https://openexchangerates.org/api/latest.json?app_id=7d48f3c6338b4e96838cf8d894162b40&symbols=PEN,USD"

    try:
        # Realizar la solicitud HTTP para obtener el JSON
        response = requests.get(url)

        # Verificar si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            # Analizar los datos JSON
            data = json.loads(response.text)

            # Obtener los valores "rates"
            rates = data["rates"]
            pen_rate = rates.get("PEN")
            usd_rate = rates.get("USD")
        else:
            # Si hay un error en la solicitud, puedes manejarlo aquí
            pen_rate = None
            usd_rate = None

    except requests.exceptions.RequestException as e:
        # Si hay un error en la solicitud, puedes manejarlo aquí
        pen_rate = None
        usd_rate = None

    # Pasar los valores como contexto al template
    return render(request, 'cambio.html', {
        'pen_rate': pen_rate,
        'usd_rate': usd_rate
    })




class DetalleEliminarView(View):

    def post(self, request, pk):
        detalle = get_object_or_404(descripcionCotizacion, pk=pk)
        cotizacion = detalle.cotizacion
        detalle.delete()

        # Recalcular y actualizar los valores de la columna "item"
        detalles = descripcionCotizacion.objects.filter(cotizacion=cotizacion)
        for index, detalle in enumerate(detalles, start=1):
            detalle.item = index
            detalle.save()

        return JsonResponse({'message': 'detalle eliminada correctamente'})

def generar_pdf(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    detalles = descripcionCotizacion.objects.filter(cotizacion=cotizacion)
    cliente = Cliente.objects.get(cliente=cotizacion.cliente)
    proforma = Proforma.objects.get(id=cotizacion.proforma.id)

    # Realizar el cálculo de los totales
    subtotal = sum(detalle.precio_total for detalle in detalles)
    igv = subtotal * Decimal('0.18')
    precio_total = subtotal + igv

    # Pasar los datos necesarios a la plantilla HTML, incluyendo los totales calculados
    context = {
        'cotizacion': cotizacion,
        'detalles': detalles,
        'cliente': cliente,
        'proforma': proforma,
        'subtotal': subtotal,
        'igv': igv,
        'precio_total': precio_total,
    }

    # Renderizar la plantilla HTML con los datos
    html = render(request, 'imprimir_detalle.html', context).content

    proforma_nombre = slugify(proforma).upper()
    nombre_archivo = f"{proforma_nombre}.pdf"

    # Crear un objeto HttpResponse para el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'

    # Convertir el HTML a PDF usando xhtml2pdf
    pisaStatus = pisa.CreatePDF(html, dest=response)

    # Comprobar si la conversión fue exitosa
    if pisaStatus.err:
        return HttpResponse('Hubo un error al generar el PDF')
    return response

#----------------MANTENIMIENTO TABLA ----------------------------
class MantenimientoView(View):

    def get(self, request):
        listaMantenimiento = piezasRepuesto.objects.all()
        context = {
            'mantenimientos': listaMantenimiento
        }
        return render(request, 'mantenimiento.html', context)
    
class  MantenimientoAgregarView(View):

    def get(self, request):
        formMantenimiento = MantenimientoForm()
        context = {
            'formMantenimiento': formMantenimiento,
        }
        return render(request, 'agregar_mantenimiento.html', context)

    def post(self, request):
        formMantenimiento = MantenimientoForm(request.POST)
        if formMantenimiento.is_valid():
            formMantenimiento.save()
            # Redirige a la lista de clientes después de guardar correctamente
            return redirect('mantenimiento')

        context = {
            'formMantenimiento': formMantenimiento,
        }
        return render(request, 'agregar_mantenimiento.html', context)
class MantenimientoEditarView(View):

    def get(self, request, pk):
        producto = get_object_or_404(piezasRepuesto, pk=pk)
        formMantenimiento = MantenimientoForm(instance=producto)
        context = {
            'formMantenimiento': formMantenimiento,
        }
        return render(request, 'agregar_mantenimiento.html', context)

    def post(self, request, pk):
        producto = get_object_or_404(piezasRepuesto, pk=pk)
        formMantenimiento = MantenimientoForm(request.POST, instance=producto)
        if formMantenimiento.is_valid():
            formMantenimiento.save()
            # Redirige a la lista de clientes después de guardar correctamente
            return redirect('mantenimiento')

        context = {
            'formMantenimieno': formMantenimiento,
        }
        return render(request, 'agregar_mantenimiento.html', context)


class MantenimientoEliminarView(View):

    def post(self, request, pk):
        producto = get_object_or_404(piezasRepuesto, pk=pk)
        producto.delete()
        return JsonResponse({'message': 'Producto eliminado correctamente'})
#----------------MANTENIMIENTO TABLA ----------------------------
class ConsultoriaView(View):

    def get(self, request):
        listaConsultoria = Consultoria.objects.all()
        context = {
            'consultorias': listaConsultoria
        }
        return render(request, 'consultoria.html', context)
    
class ConsultoriaAgregarView(View):

    def get(self, request):
        formConsultoria = ConsultoriaForm()
        context = {
            'formConsultoria': formConsultoria,
        }
        return render(request, 'agregar_consultoria.html', context)

    def post(self, request):
        formConsultoria = ConsultoriaForm(request.POST)
        if formConsultoria.is_valid():
            formConsultoria.save()
            # Redirige a la lista de clientes después de guardar correctamente
            return redirect('consultoria')

        context = {
            'formConsultoria': formConsultoria,
        }
        return render(request, 'agregar_consultoria.html', context)


class ConsultoriaEditarView(View):

    def get(self, request, pk):
        consultoria = get_object_or_404(Consultoria, pk=pk)
        formConsultoria = ConsultoriaForm(instance=consultoria)
        context = {
            'formConsultoria': formConsultoria,
        }
        return render(request, 'agregar_consultoria.html', context)

    def post(self, request, pk):
        consultoria = get_object_or_404(Consultoria, pk=pk)
        formConsultoria = ConsultoriaForm(request.POST, instance=consultoria)
        if formConsultoria.is_valid():
            formConsultoria.save()
            # Redirige a la lista de clientes después de guardar correctamente
            return redirect('consultoria')

        context = {
            'formConsultoria': formConsultoria,
        }
        return render(request, 'agregar_consultoria.html', context)
    
class ConsultoriaEliminarView(View):

    def post(self, request, pk):
        consultoria = get_object_or_404(Consultoria, pk=pk)
        consultoria.delete()
        return JsonResponse({'message': 'Consultoria eliminada correctamente'})
#----------------MANTENIMIENTO TABLA ----------------------------
class ManoDeObraView(View):

    def get(self, request):
        listaManodeobras = ManodeObra.objects.all()
        context = {
            'obras': listaManodeobras
        }
        return render(request, 'obra.html', context)
    
class ManoDeObraAgregarView(View):

    def get(self, request):
        formManodeObra = ManoDeObraForm()
        context = {
            'formManodeObra': formManodeObra,
        }
        return render(request, 'agregar_obra.html', context)

    def post(self, request):
        formManodeObra = ManoDeObraForm(request.POST)
        if formManodeObra.is_valid():
            formManodeObra.save()
            # Redirige a la lista de clientes después de guardar correctamente
            return redirect('manodeobra')

        context = {
            'formManodeObra': formManodeObra,
        }
        return render(request, 'agregar_obra.html', context)


class ManoDeObraEditarView(View):

    def get(self, request, pk):
        manodeobra = get_object_or_404(ManodeObra, pk=pk)
        formManodeObra = ManoDeObraForm(instance=manodeobra)
        context = {
            'formManodeObra': formManodeObra,
        }
        return render(request, 'agregar_obra.html', context)

    def post(self, request, pk):
        manodeobra = get_object_or_404(ManodeObra, pk=pk)
        formManodeObra = ManoDeObraForm(request.POST, instance=manodeobra)
        if formManodeObra.is_valid():
            formManodeObra.save()
            # Redirige a la lista de clientes después de guardar correctamente
            return redirect('manodeobra')

        context = {
            'formManodeObra': formManodeObra,
        }
        return render(request, 'agregar_obra.html', context)
    
class ManoDeObraEliminarView(View):

    def post(self, request, pk):
        manodeobra = get_object_or_404(ManodeObra, pk=pk)
        manodeobra.delete()
        return JsonResponse({'message': 'Mano De obra eliminada correctamente'})
