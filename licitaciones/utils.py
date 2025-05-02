import requests

API_URL = "http://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json"
API_KEY = "F8537A18-6766-4DEF-9E59-426B4FEE2844"  # Reemplázalo por tu ticket real

def buscar_licitaciones_api(texto_busqueda):
    params = {
        "estado": "publicada",     # puedes cambiar por 'todas'
        "palabra": texto_busqueda,
        "ticket": API_KEY
    }

    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("Listado", [])
    except Exception as e:
        print("Error al conectar con la API de Mercado Público:", e)
        return []
