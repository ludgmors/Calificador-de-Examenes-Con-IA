import easyocr

def extraer_texto(ruta_imagen):
    lector = easyocr.Reader(['es'], gpu=False)
    resultado = lector.readtext(ruta_imagen, detail=0)
    return "\n".join(resultado)

# Prueba directa
if __name__ == "__main__":
    texto = extraer_texto("imagenes/ejemplo.jpg")
    print("Texto detectado:")
    print(texto)
