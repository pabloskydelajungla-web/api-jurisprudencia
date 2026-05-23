from fastapi import FastAPI, Query
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

app = FastAPI(title="API Jurisprudencia Española")

@app.get("/")
def home():
    return {
        "status": "ok",
        "message": "API jurisprudencia funcionando"
    }

@app.get("/jurisprudencia/buscar")
def buscar_jurisprudencia(
    q: str = Query(...),
    tribunal: str | None = None
):
    busqueda = q
    if tribunal:
        busqueda += f" {tribunal}"

    # Búsqueda pública limitada sobre Poder Judicial / CENDOJ
    url_busqueda = (
        "https://www.google.com/search?q="
        + quote_plus(f'site:poderjudicial.es/search/ {busqueda} jurisprudencia CENDOJ')
    )

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(url_busqueda, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        resultados = []

        for item in soup.select("a"):
            href = item.get("href", "")
            texto = item.get_text(" ", strip=True)

            if "poderjudicial.es" in href and texto:
                resultados.append({
                    "id": f"resultado-{len(resultados)+1}",
                    "tribunal": tribunal or "No especificado",
                    "fecha": "No extraída",
                    "titulo": texto[:180],
                    "resumen": "Resultado localizado en fuente pública relacionada con Poder Judicial/CENDOJ.",
                    "url": href
                })

            if len(resultados) >= 5:
                break

        if not resultados:
            resultados = [{
                "id": "sin-resultados",
                "tribunal": tribunal or "No especificado",
                "fecha": "No extraída",
                "titulo": f"Búsqueda CENDOJ para: {busqueda}",
                "resumen": "No se pudieron extraer resultados automáticamente. Consulta manual recomendada en el buscador oficial.",
                "url": "https://www.poderjudicial.es/search/indexAN.jsp"
            }]

        return {"resultados": resultados}

    except Exception as e:
        return {
            "resultados": [{
                "id": "error",
                "tribunal": tribunal or "No especificado",
                "fecha": "No extraída",
                "titulo": "Error buscando jurisprudencia",
                "resumen": str(e),
                "url": "https://www.poderjudicial.es/search/indexAN.jsp"
            }]
        }

@app.get("/jurisprudencia/sentencia/{id}")
def obtener_sentencia(id: str):
    return {
        "id": id,
        "tribunal": "No especificado",
        "fecha": "No extraída",
        "titulo": "Detalle no disponible automáticamente",
        "fundamentos": "Esta versión inicial de la API busca resultados públicos, pero todavía no extrae el texto completo de la sentencia.",
        "fallo": "No disponible.",
        "url": "https://www.poderjudicial.es/search/indexAN.jsp"
    }
