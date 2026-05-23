from fastapi import FastAPI, Query
from urllib.parse import quote_plus

app = FastAPI(title="API Jurisprudencia y Fuentes Oficiales")

FUENTES_PERMITIDAS = {
    "boe": {
        "nombre": "BOE",
        "dominio": "boe.es",
        "url": "https://www.boe.es"
    },
    "cendoj": {
        "nombre": "CENDOJ / Poder Judicial",
        "dominio": "poderjudicial.es",
        "url": "https://www.poderjudicial.es/search/indexAN.jsp"
    },
    "poder_judicial": {
        "nombre": "Poder Judicial",
        "dominio": "poderjudicial.es",
        "url": "https://www.poderjudicial.es"
    },
    "tribunal_constitucional": {
        "nombre": "Tribunal Constitucional",
        "dominio": "tribunalconstitucional.es",
        "url": "https://hj.tribunalconstitucional.es"
    },
    "boc": {
        "nombre": "BOC - Boletín Oficial de Canarias",
        "dominio": "gobiernodecanarias.org",
        "url": "https://www.gobiernodecanarias.org/boc/"
    },
    "vlex": {
        "nombre": "vLex",
        "dominio": "vlex.es",
        "url": "https://vlex.es"
    }
}


@app.get("/")
def home():
    return {
        "status": "ok",
        "message": "API funcionando solo con fuentes permitidas",
        "fuentes_permitidas": [
            "BOE",
            "CENDOJ",
            "Poder Judicial",
            "Tribunal Constitucional",
            "BOC",
            "vLex"
        ]
    }


@app.get("/fuentes")
def fuentes():
    return FUENTES_PERMITIDAS


@app.get("/jurisprudencia/buscar")
def buscar_jurisprudencia(
    q: str = Query(...),
    tribunal: str | None = None
):
    busqueda = q

    if tribunal:
        busqueda = f"{q} {tribunal}"

    url_cendoj = (
        "https://www.poderjudicial.es/search/indexAN.jsp"
        f"?texto={quote_plus(busqueda)}"
    )

    url_tc = (
        "https://hj.tribunalconstitucional.es"
        f"?q={quote_plus(busqueda)}"
    )

    return {
        "resultados": [
            {
                "id": "busqueda-cendoj",
                "fuente": "CENDOJ / Poder Judicial",
                "dominio": "poderjudicial.es",
                "tribunal": tribunal or "No especificado",
                "fecha": "No extraída",
                "titulo": f"Búsqueda oficial CENDOJ: {busqueda}",
                "resumen": "Búsqueda jurisprudencial preparada en fuente oficial. No representa todavía una sentencia concreta.",
                "url": url_cendoj,
                "tipo": "busqueda_oficial"
            },
            {
                "id": "busqueda-tribunal-constitucional",
                "fuente": "Tribunal Constitucional",
                "dominio": "tribunalconstitucional.es",
                "tribunal": "Tribunal Constitucional",
                "fecha": "No extraída",
                "titulo": f"Búsqueda Tribunal Constitucional: {busqueda}",
                "resumen": "Búsqueda preparada en la base oficial de jurisprudencia constitucional.",
                "url": url_tc,
                "tipo": "busqueda_oficial"
            }
        ]
    }


@app.get("/jurisprudencia/sentencia/{id}")
def obtener_sentencia(id: str):
    return {
        "id": id,
        "fuente": "CENDOJ / Poder Judicial",
        "dominio": "poderjudicial.es",
        "tribunal": "No especificado",
        "fecha": "No extraída",
        "titulo": "Sentencia no extraída automáticamente",
        "fundamentos": "Esta API todavía no descarga sentencias completas. Solo prepara búsquedas en fuentes oficiales permitidas.",
        "fallo": "No disponible",
        "url": "https://www.poderjudicial.es/search/indexAN.jsp"
    }


@app.get("/buscar-oficial")
def buscar_oficial(
    q: str = Query(...),
    fuente: str | None = None
):
    fuentes_a_usar = FUENTES_PERMITIDAS

    if fuente:
        clave = fuente.lower().replace(" ", "_")
        fuentes_a_usar = {
            k: v for k, v in FUENTES_PERMITIDAS.items()
            if clave in k or clave in v["nombre"].lower().replace(" ", "_")
        }

    resultados = []

    for clave, datos in fuentes_a_usar.items():
        dominio = datos["dominio"]
        nombre = datos["nombre"]

        if clave == "cendoj":
            url = (
                "https://www.poderjudicial.es/search/indexAN.jsp"
                f"?texto={quote_plus(q)}"
            )
        elif clave == "tribunal_constitucional":
            url = (
                "https://hj.tribunalconstitucional.es"
                f"?q={quote_plus(q)}"
            )
        elif clave == "boc":
            url = (
                "https://www.gobiernodecanarias.org/boc/"
            )
        else:
            url = (
                f"https://www.google.com/search?q="
                f"{quote_plus('site:' + dominio + ' ' + q)}"
            )

        resultados.append({
            "id": f"busqueda-{clave}",
            "fuente": nombre,
            "dominio": dominio,
            "titulo": f"Búsqueda oficial en {nombre}: {q}",
            "resumen": "Resultado limitado a fuente permitida. No usar fuentes externas no incluidas en la lista blanca.",
            "url": url,
            "tipo": "busqueda_oficial"
        })

    return {
        "consulta": q,
        "fuentes_permitidas": [
            "BOE",
            "CENDOJ",
            "Poder Judicial",
            "Tribunal Constitucional",
            "BOC",
            "vLex"
        ],
        "resultados": resultados
    }
