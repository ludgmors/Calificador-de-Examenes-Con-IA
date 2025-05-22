from fpdf import FPDF

class ExportadorPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Resultados del Examen', border=False, ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def exportar_a_pdf(resultados, nombre_estudiante, carrera, semestre, seccion="", total_100=None, nombre_archivo="resultados_examen.pdf"):
    pdf = ExportadorPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Encabezado
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Estudiante: {nombre_estudiante}", ln=True)
    if carrera:
        pdf.cell(0, 10, f"carrera: {carrera}", ln=True)
    if semestre:
        pdf.cell(0, 10, f"Semestre: {semestre}", ln=True)
    if seccion:
        pdf.cell(0, 10, f"Sección: {seccion}", ln=True)
    if total_100 is not None:
        pdf.cell(0, 10, f"Puntaje total: {total_100} / 100", ln=True)
    pdf.ln(5)

    # Pregunta por pregunta

    for i, item in enumerate(resultados, 1):
        pdf.set_font("Arial", "B", 12)
        pdf.multi_cell(0, 10, f"Pregunta {i}: {item['pregunta']}")
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, f"Respuesta del estudiante: {item['respuesta_estudiante']}")
        pdf.multi_cell(0, 10, f"Respuesta ideal: {item['respuesta_ideal']}")
        pdf.multi_cell(0, 10, f"Resultado del análisis:\n{item['resultado_analisis']}")
        pdf.ln(5)

    
    pdf.output(nombre_archivo)
    return nombre_archivo