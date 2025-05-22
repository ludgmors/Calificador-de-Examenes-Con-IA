from lector_ocr.lector_texto import extraer_texto
from modelo_lenguaje.calificador import calificar_respuesta
from utilidades.herramientas import limpiar_texto_ocr, extraer_preguntas_respuestas
from utilidades.lector_pdf import leer_respuestas_desde_pdf
from utilidades.lector_documento import extraer_texto_pdf, extraer_texto_docx
from utilidades.generador_pdf import exportar_resultados_pdf

# 1. Cargar imagen del examen
ruta_imagen = "imagenes/ejemplo.jpg"
tipo_examen = "pdf"  # opciones: "imagen", "pdf", "word"

# 2. Extraer texto desde la imagen
if tipo_examen == "imagen":
    ruta = "imagenes/ejemplo.jpg"
    texto_crudo = extraer_texto(ruta)
elif tipo_examen == "pdf":
    ruta = "examen.pdf"  # asegúrate de tener este archivo en la raíz o en documentos/
    texto_crudo = extraer_texto_pdf(ruta)
elif tipo_examen == "word":
    ruta = "examen.docx"
    texto_crudo = extraer_texto_docx(ruta)
else:
    raise ValueError("Tipo de examen no soportado.")



texto_extraido = limpiar_texto_ocr(texto_crudo)



print("📝 Texto extraído limpio:")
print(texto_extraido)

# 3. Separar en bloques de preguntas y respuestas
bloques = extraer_preguntas_respuestas(texto_extraido)

from utilidades.lector_pdf import leer_respuestas_desde_pdf

# Ruta del PDF con las respuestas correctas
ruta_pdf = "Respuestas.pdf"

# Leer respuestas ideales desde el PDF
respuestas_ideales = leer_respuestas_desde_pdf(ruta_pdf)

# 5. Calificar cada bloque
for i, (pregunta, respuesta_estudiante) in enumerate(bloques, 1):
    print(f"\n📌 Pregunta {i}: {pregunta}")
    print(f"✍️ Respuesta del estudiante: {respuesta_estudiante}")

    
    clave = pregunta.lower().replace("¿", "").replace("?", "").strip()
    respuesta_ideal = respuestas_ideales.get(clave, "Respuesta ideal no definida para esta pregunta.")
    resultado = calificar_respuesta(pregunta, respuesta_estudiante, respuesta_ideal, nivel_exigencia=5)
    
    print("📊 Resultado del análisis:")
    print(resultado)


resultados_para_pdf = []

for i, (pregunta, respuesta_estudiante) in enumerate(bloques, 1):
    clave = pregunta.lower().replace("¿", "").replace("?", "").strip()
    respuesta_ideal = respuestas_ideales.get(clave, "Respuesta ideal no definida para esta pregunta.")
    resultado = calificar_respuesta(pregunta, respuesta_estudiante, respuesta_ideal, nivel_exigencia=5)

    print(f"\n📌 Pregunta {i}: {pregunta}")
    print(f"✍️ Respuesta del estudiante: {respuesta_estudiante}")
    print("📊 Resultado del análisis:")
    print(resultado)

    resultados_para_pdf.append((pregunta, respuesta_estudiante, respuesta_ideal, resultado))

# Exportar informe
exportar_resultados_pdf("informe_calificacion.pdf", resultados_para_pdf)


