from fastapi import FastAPI, Query
from urllib.parse import quote_plus

app = FastAPI(title="API Jurisprudencia Española")

CENDOJ_URL = "https://www.poderjudicial.es/search/indexAN.jsp"

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
        busqueda = f"{q} {tribunal}"

    url_busqueda = f"{CENDOJ_URL}?texto={quote_plus(busqueda)}"

    return {
        "resultados": [
            {
                "id": "busqueda-cendoj",
                "tribunal": tribunal or "No especificado",
                "fecha": "No extraída",
                "titulo": f"Búsqueda oficial CENDOJ: {busqueda}",
                "resumen": "Se ha preparado una búsqueda en el buscador oficial del Poder Judicial/CENDOJ. Esta respuesta no representa todavía una sentencia concreta.",
                "url": url_busqueda,
                "tipo": "busqueda_oficial"
            }
        ]
    }

@app.get("/jurisprudencia/sentencia/{id}")
def obtener_sentencia(id: str):
    return {
        "id": id,
        "tribunal": "No especificado",
        "fecha": "No extraída",
        "titulo": "Sentencia no extraída automáticamente",
        "fundamentos": "Esta API todavía no extrae el texto completo de sentencias. Usa primero el enlace oficial CENDOJ devuelto por la búsqueda.",
        "fallo": "No disponible.",
        "url": CENDOJ_URL
    }from fastapi import FastAPI, Query
from urllib.parse import quote_plus

app = FastAPI(title="API Jurisprudencia Española")

CENDOJ_URL = "https://www.poderjudicial.es/search/indexAN.jsp"

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
        busqueda = f"{q} {tribunal}"

    url_busqueda = f"{CENDOJ_URL}?texto={quote_plus(busqueda)}"

    return {
        "resultados": [
            {
                "id": "busqueda-cendoj",
                "tribunal": tribunal or "No especificado",
                "fecha": "No extraída",
                "titulo": f"Búsqueda oficial CENDOJ: {busqueda}",
                "resumen": "Se ha preparado una búsqueda en el buscador oficial del Poder Judicial/CENDOJ. Esta respuesta no representa todavía una sentencia concreta.",
                "url": url_busqueda,
                "tipo": "busqueda_oficial"
            }
        ]
    }

@app.get("/jurisprudencia/sentencia/{id}")
def obtener_sentencia(id: str):
    return {
        "id": id,
        "tribunal": "No especificado",
        "fecha": "No extraída",
        "titulo": "Sentencia no extraída automáticamente",
        "fundamentos": "Esta API todavía no extrae el texto completo de sentencias. Usa primero el enlace oficial CENDOJ devuelto por la búsqueda.",
        "fallo": "No disponible.",
        "url": CENDOJ_URL
    }
