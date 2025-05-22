import fitz  # PyMuPDF

def leer_respuestas_desde_pdf(ruta_pdf):
    doc = fitz.open(ruta_pdf)
    texto_total = ""

    for pagina in doc:
        texto_total += pagina.get_text()

    # Extraer pares pregunta:respuesta del texto
    lineas = texto_total.splitlines()
    respuestas = {}

    for linea in lineas:
        if ":" in linea:
            partes = linea.split(":", 1)
            pregunta = partes[0].strip().lower().replace("¿", "").replace("?", "").replace('"', '')
            respuesta = partes[1].strip().strip('"')
            respuestas[pregunta] = respuesta

    return respuestas
