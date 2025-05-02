from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from licitaciones.models import Licitacion
from django.utils.timezone import make_aware
from django.db.models import Count
from django.db.models.functions import TruncMonth
import csv
from datetime import datetime
import io
from licitaciones.forms import UploadCSVForm


@login_required
def home_view(request):
    form_csv = UploadCSVForm()

    if request.method == 'POST' and request.FILES.get('archivo'):
        form_csv = UploadCSVForm(request.POST, request.FILES)
        if form_csv.is_valid():
            archivo = request.FILES['archivo']
            decoded = archivo.read().decode('utf-8').replace('\ufeff', '')
            reader = csv.DictReader(io.StringIO(decoded), delimiter=';')

            for row in reader:
                try:
                    fecha = make_aware(datetime.strptime(row['FechaPublicacion'], "%d/%m/%Y %H:%M:%S"))
                    Licitacion.objects.update_or_create(
                        id_licitacion=row.get('IDLicitacion') or row.get('﻿IDLicitacion'),
                        defaults={
                            'nombre': row.get('NombreLicitacion', ''),
                            'tipo': row.get('Tipo', ''),
                            'estado': row.get('Estado', ''),
                            'fecha_publicacion': fecha,
                            'descripcion': row.get('Descripcion', ''),
                            'moneda': row.get('Moneda', ''),
                            'tipo_presupuesto': row.get('TipoPresupuesto', ''),
                            'tipo_monto': row.get('TipoMonto', ''),
                            'monto': row.get('MontoLicitacion', ''),
                            'organismo': row.get('Organismo', ''),
                            'detalle_url': f"https://www.mercadopublico.cl/Home/ShowLicitacion?id={row.get('IDLicitacion')}"
                        }
                    )
                except Exception as e:
                    print(f"⚠️ Error con licitación {row.get('IDLicitacion', '???')}: {e}")
            return redirect('home')

    texto = request.GET.get('q', '')
    licitaciones = Licitacion.objects.filter(nombre__icontains=texto) if texto else Licitacion.objects.all()

    return render(request, 'home/home.html', {
        'user': request.user,
        'form_csv': form_csv,
        'licitaciones': licitaciones,
        'texto': texto
    })


@login_required
def dashboard_view(request):
    total_licitaciones = Licitacion.objects.count()
    monto_total = Licitacion.objects.exclude(monto="").count()  # opcional: sumar con Decimal

    tipos = Licitacion.objects.values('tipo').annotate(cantidad=Count('id_licitacion')).order_by('-cantidad')
    organismos = Licitacion.objects.values('organismo').annotate(cantidad=Count('id_licitacion')).order_by('-cantidad')[:3]

    publicaciones_por_mes = (
        Licitacion.objects
        .annotate(mes=TruncMonth('fecha_publicacion'))
        .values('mes')
        .annotate(cantidad=Count('id_licitacion'))
        .order_by('mes')
    )

    licitaciones_recientes = Licitacion.objects.order_by('-fecha_publicacion')[:5]

    return render(request, 'home/dashboard.html', {
        'total_licitaciones': total_licitaciones,
        'monto_total': monto_total,
        'tipos': tipos,
        'organismos': organismos,
        'publicaciones_por_mes': publicaciones_por_mes,
        'licitaciones_recientes': licitaciones_recientes
    })
