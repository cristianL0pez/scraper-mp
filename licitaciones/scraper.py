import requests
from bs4 import BeautifulSoup

def buscar_licitaciones_scraper(texto_busqueda):
    url = f"https://www.mercadopublico.cl/Home/SearchLicitacion?query={texto_busqueda}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error al conectar: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    resultados = []

    for row in soup.select(".contenedorResultadoBusqueda"):
        nombre = row.select_one(".nombreLicitacion a")
        codigo = row.select_one(".codigoLicitacion")
        organismo = row.select_one(".organismoLicitacion")

        if nombre and codigo:
            resultados.append({
                "nombre": nombre.text.strip(),
                "link": "https://www.mercadopublico.cl" + nombre['href'],
                "codigo": codigo.text.strip(),
                "organismo": organismo.text.strip() if organismo else "",
            })

    return resultados
