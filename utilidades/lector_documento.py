import fitz  # PyMuPDF
from docx import Document

def extraer_texto_pdf(ruta_pdf):
    doc = fitz.open(ruta_pdf)
    texto_total = ""
    for pagina in doc:
        texto_total += pagina.get_text()
    return texto_total

def extraer_texto_docx(ruta_docx):
    doc = Document(ruta_docx)
    texto = "\n".join([p.text for p in doc.paragraphs])
    return texto
