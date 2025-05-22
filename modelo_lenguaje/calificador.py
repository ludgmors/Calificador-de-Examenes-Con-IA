import ollama

def calificar_respuesta(pregunta, respuesta_estudiante, respuesta_esperada, nivel_exigencia=5):
    prompt = f"""
Eres un profesor universitario corrigiendo exámenes de forma automática. Tu tarea es calificar respuestas de estudiantes usando únicamente una escala binaria: 0 o 10.

- Si la respuesta del estudiante coincide claramente con la respuesta ideal (aunque con palabras diferentes pero mismo significado), asigna un **10**.
- Si la respuesta es incorrecta, irrelevante o no responde a lo que se pregunta, asigna un **0**.
- No uses ningún otro valor intermedio.
- Sé estricto pero justo: no penalices redacción o estilo si la idea es correcta.

Pregunta: {pregunta}

Respuesta del estudiante: {respuesta_estudiante}

Respuesta ideal: {respuesta_esperada}

Indica la calificación (0 o 10) y da una breve justificación.

"""

    respuesta = ollama.chat(
        model='llama3',  # o el modelo que consideren, yo este use okey >:{

        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return respuesta['message']['content']
