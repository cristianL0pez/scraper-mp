import csv
from datetime import datetime
from django.utils.timezone import make_aware
from licitaciones.models import Licitacion

def importar_csv(filepath):
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader((line.replace('\ufeff', '') for line in csvfile), delimiter=';')
        print("Headers detectados:", reader.fieldnames)
        for row in reader:
            try:
                fecha = make_aware(datetime.strptime(row['FechaPublicacion'], "%d/%m/%Y %H:%M:%S"))
                Licitacion.objects.update_or_create(
                    id_licitacion=row['IDLicitacion'],
                    defaults={
                        'nombre': row['NombreLicitacion'],
                        'tipo': row['Tipo'],
                        'estado': row['Estado'],
                        'fecha_publicacion': fecha,
                        'descripcion': row['Descripcion'],
                        'moneda': row['Moneda'],
                        'tipo_presupuesto': row['TipoPresupuesto'],
                        'tipo_monto': row['TipoMonto'],
                        'monto': row['MontoLicitacion'],
                        'organismo': row['Organismo']
                    }
                )
            except Exception as e:
                print(f"⚠️ Error con licitación {row.get('IDLicitacion', 'desconocida')}: {e}")
