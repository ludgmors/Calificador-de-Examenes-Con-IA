import streamlit as st
from lector_ocr.lector_texto import extraer_texto
from utilidades.herramientas import limpiar_texto_ocr, extraer_preguntas_respuestas
from modelo_lenguaje.calificador import calificar_respuesta
from utilidades.lector_pdf import leer_respuestas_desde_pdf
import tempfile
import os
from utilidades.generador_pdf import exportar_a_pdf

st.set_page_config(page_title="Calificador Inteligente de Exámenes", layout="centered")

st.markdown("""
    <style>
        /* Fondo general con degradado suave */
        .main {
            background: linear-gradient(to right, #f8f9fa, #e9ecef);
            color: #333;
            padding: 2rem;
            font-family: 'Segoe UI', sans-serif;
        }

        /* Centrado del título principal */
        h1 {
            text-align: center;
            color: #343a40;
            font-size: 2.5rem;
        }

        /* Espacio para todo el contenido */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            background-color: #87CEEB;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(4px);
        }

        /* Títulos secundarios */
        h2, h3 {
            color: #495057;
        }

        /* Inputs y botones Streamlit */
        .stTextInput > div > input,
        .stTextArea textarea,
        .stFileUploader {
            border: 1px solid #ced4da;
            border-radius: 10px;
            padding: 10px;
            background-color: #f8f9fa;
        }

        .stButton > button {
            background-color: #4CAF50;
            color: white;
            padding: 0.6rem 1.2rem;
            border: none;
            border-radius: 10px;
            transition: background-color 0.3s;
        }

        .stButton > button:hover {
            background-color: #45a049;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 Calificador de Exámenes con IA")
st.write("Sube una imagen del examen y un archivo PDF con las respuestas correctas.")


# 1. Cargar archivo del examen (imagen, PDF o Word)                 perro el que lo lea :)
archivo_examen = st.file_uploader("📄 Sube el examen (imagen, PDF o Word)", type=["jpg", "jpeg", "png", "pdf", "docx"])


# 2. Cargar PDF de respuestas
pdf = st.file_uploader("📄 Sube el PDF con las respuestas ideales", type=["pdf"])

# 3. Nivel de exigencia
nivel = st.slider("⚙️ Nivel de exigencia", 1, 10, 5)

# 4. Botón para procesar
col1, col2, col3, col4 = st.columns(4)
with col1:
    nombre_estudiante = st.text_input("👤 Nombre del estudiante")
with col2:
    carrera = st.text_input("🏁 carrera")    
with col3:
    semestre = st.text_input("📘 Semestre")
with col4:
    seccion = st.text_input("🏫 Sección")
if st.button("🔍 Calificar examen"):
    if archivo_examen and pdf and nombre_estudiante.strip() and carrera.strip() and semestre.strip() and seccion.strip():

    
     with st.spinner("Procesando examen..."):
        # Guardar archivos temporalmente
        tipo_archivo = archivo_examen.name.split(".")[-1].lower()

        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{tipo_archivo}") as tmp_exam:
            tmp_exam.write(archivo_examen.read())
            ruta_examen = tmp_exam.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            tmp_pdf.write(pdf.read())
            ruta_pdf = tmp_pdf.name

        # Leer respuestas correctas
        respuestas_ideales = leer_respuestas_desde_pdf(ruta_pdf)

        # Leer texto del examen según el tipo
        if tipo_archivo in ["jpg", "jpeg", "png"]:
            texto = extraer_texto(ruta_examen)
        elif tipo_archivo == "pdf":
            from utilidades.lector_documento import extraer_texto_pdf
            texto = extraer_texto_pdf(ruta_examen)
        elif tipo_archivo == "docx":
            from utilidades.lector_documento import extraer_texto_docx
            texto = extraer_texto_docx(ruta_examen)
        else:
            st.error("Formato de archivo no soportado.")
            texto = ""

        # Procesar texto
        texto_limpio = limpiar_texto_ocr(texto)
        bloques = extraer_preguntas_respuestas(texto_limpio)
        st.info(f"🧩 Se detectaron {len(bloques)} bloques de pregunta-respuesta.")


        st.subheader("📋 Resultados")
        resultados = []
        import re
        punteos = []

        if not bloques:
            st.error("No se detectaron preguntas y respuestas válidas en el archivo.")
        else:
            for i, (pregunta, respuesta_estudiante) in enumerate(bloques, 1):
                clave = pregunta.lower().replace("¿", "").replace("?", "").strip()
                respuesta_ideal = respuestas_ideales.get(clave, "Respuesta ideal no definida para esta pregunta.")
                resultado = calificar_respuesta(pregunta, respuesta_estudiante, respuesta_ideal, nivel)

                resultados.append({
                    "pregunta": pregunta,
                    "respuesta_estudiante": respuesta_estudiante,
                    "respuesta_ideal": respuesta_ideal,
                    "resultado_analisis": resultado.strip() 
                })

                with st.expander(f"🔹 Pregunta {i}"):
                    st.markdown(f"**Pregunta:** {pregunta}")
                    st.markdown(f"**Respuesta del estudiante:** {respuesta_estudiante}")
                    st.markdown(f"**Respuesta ideal:** {respuesta_ideal}")
                    st.markdown(f"**Resultado del análisis:**\n\n{resultado}")

        punteos = []
        for item in resultados:
                analisis = item["resultado_analisis"]
                #st.text(analisis)
                match = re.search(r"Cal[ií]f[ií]caci[oó]n\s*[:\-]?\s*\*{0,2}(\d{1,2})\*{0,2}", analisis, re.IGNORECASE)
                if not match:
                    match = re.search(r"\b([01]0)\b", analisis.strip())
                if match:
                    try:
                        puntaje = int(match.group(1).strip())
                        if puntaje in [0, 10]:
                            punteos.append(puntaje)
                    except ValueError:
                        continue
                        
        st.info(f"📊 Puntajes detectados: {punteos}")
                                                                                                                                                    
        if punteos:
               promedio = sum(punteos) / len(punteos)
               total_100 = round(promedio * 10, 2)
               st.success(f"🎯 Puntaje total de {nombre_estudiante}: {total_100} / 100")
        else:
                total_100 = None
                st.warning("⚠️ No se detectaron calificaciones numéricas.")
        
    
        if resultados:
            nombre_pdf = exportar_a_pdf(

                resultados,
                nombre_estudiante=nombre_estudiante,
                total_100=total_100,
                carrera=carrera,
                semestre=semestre,
                seccion=seccion
             )
            with open(nombre_pdf, "rb") as f:
                 st.download_button(
                  label="📥 Descargar resultados en PDF",
                  data=f,
                  file_name=f"resultados_{nombre_estudiante.replace(' ', '_')}.pdf",
                  mime="application/pdf"
              )
    

        # Eliminar archivos temporales
        os.unlink(ruta_examen)
        os.unlink(ruta_pdf)

else:
    st.warning("Debes subir tanto una (imagen, pdf o word) del examen, como el PDF de las respuestas.")


#Hecho por Ludwing Morales 1590-21-18758

#streamlit run interfaz.py
