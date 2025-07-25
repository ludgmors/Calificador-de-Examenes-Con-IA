# 🧠 Calificador Inteligente de Exámenes

Sistema de calificación automática que utiliza OCR y modelos de lenguaje para evaluar respuestas escritas de estudiantes. Ideal para docentes que desean corregir exámenes, rápido y objetivamente con retroalimentación clara.

## 🚀 Características

- 📸 Soporte para imágenes escaneadas, PDF y documentos Word (.docx).
- 📄 Carga de respuestas ideales desde un PDF.
- 🧠 Calificación automática usando Llama3 vía Ollama.
- 🎯 Evaluación binaria: 0 (incorrecto) o 10 (correcto).
- 🔍 Puntaje final sobre 100 con promedio calculado.
- 📝 Justificación por cada calificación.
- 📥 Exportación de resultados a PDF profesional.
- 💬 Conclusión general con sugerencias de mejora.
- 🎨 Interfaz moderna con fondo personalizado (Streamlit).

## 📦 Requisitos

- Python 3.10 o superior
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (si usarás imágenes)
- [Ollama](https://ollama.com/) para usar el modelo localmente
- Dependencias de Python:

```bash
pip install -r requirements.txt

🛠️ Estructura del Proyecto
ProyectoIA/
├── interfaz.py
├── modelo_lenguaje/
│   └── calificador.py
├── utilidades/
│   ├── generador_pdf.py
│   ├── herramientas.py
│   ├── lector_pdf.py
│   └── lector_documento.py
├── lector_ocr/
│   └── lector_texto.py
├── assets/
├── requirements.txt

💡 ¿Cómo funciona?
Subes el examen del estudiante (imagen, PDF o Word).

Subes un PDF con las respuestas ideales.

El sistema extrae preguntas y respuestas.

Compara y califica con un modelo de lenguaje (0 o 10).

Genera resultados detallados con retroalimentación y un PDF.

🧠 Modelo de Lenguaje
Utiliza llama3 vía Ollama

Puedes cambiar el modelo o nivel de exigencia en calificador.py.

📬 Contacto
¿Tienes dudas, sugerencias o deseas colaborar?

Ludwing Danilo Morales De Paz
💻 GitHub:https://github.com/ludgmors
🎓 Estudiante de Ingeniería en Sistemas

📝 Licencia
Este proyecto está bajo la licencia MIT. Puedes usarlo, modificarlo y distribuirlo libremente, dando el crédito correspondiente.
