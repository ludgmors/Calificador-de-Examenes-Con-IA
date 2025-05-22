
def limpiar_texto_ocr(texto):

    lineas = texto.split("\n")
    nuevas_lineas = []

    linea_actual = ""
    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue

        # Si es una nueva pregunta o respuesta, guarda la anterior
        if linea.lower().startswith("pregunta:") or linea.lower().startswith("respuesta:"):
            if linea_actual:
                nuevas_lineas.append(linea_actual)
            linea_actual = linea
        else:
            # Si no empieza con "Pregunta" o "Respuesta", es una continuación de la anterior
            linea_actual += " " + linea

    # Agregar la última línea
    if linea_actual:
        nuevas_lineas.append(linea_actual)

    return "\n".join(nuevas_lineas)

import re

def extraer_preguntas_respuestas(texto):
    
    patron = r"Pregunta:\s*(.*?)\s*Respuesta:\s*(.*?)(?=(\nPregunta:|\Z))"
    bloques = re.findall(patron, texto, re.DOTALL | re.IGNORECASE)

    lista = []
    for pregunta, respuesta, _ in bloques:
        lista.append((pregunta.strip(), respuesta.strip()))
    
    return lista


