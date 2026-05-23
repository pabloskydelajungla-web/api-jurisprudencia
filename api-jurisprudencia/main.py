from fastapi import FastAPI, Query

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
    tribunal: str | None = None,
    desde: str | None = None,
    hasta: str | None = None
):
    return {
        "resultados": [
            {
                "id": "demo-1",
                "tribunal": tribunal or "Tribunal Supremo",
                "fecha": "2024-01-01",
                "titulo": f"Resultado demo sobre {q}",
                "resumen": "Respuesta de prueba. Después conectaremos CENDOJ real.",
                "url": "https://www.poderjudicial.es"
            }
        ]
    }

@app.get("/jurisprudencia/sentencia/{id}")
def obtener_sentencia(id: str):
    return {
        "id": id,
        "tribunal": "Tribunal Supremo",
        "fecha": "2024-01-01",
        "titulo": "Sentencia demo",
        "fundamentos": "Fundamentos jurídicos de prueba.",
        "fallo": "Fallo de prueba.",
        "url": "https://www.poderjudicial.es"
    }