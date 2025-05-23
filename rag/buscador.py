from sentence_transformers import SentenceTransformer
import faiss
import pickle

modelo = SentenceTransformer('all-MiniLM-L6-v2')

def buscar_contexto(pregunta, nombre_indice='indice_faiss', k=3):
    # Cargar índice y textos
    index = faiss.read_index(f"{nombre_indice}.index")
    with open(f"{nombre_indice}_documentos.pkl", "rb") as f:
        documentos = pickle.load(f)

    # Convertir pregunta a embedding y buscar
    embedding = modelo.encode([pregunta])
    distancias, indices = index.search(embedding, k)

    resultados = [documentos[i] for i in indices[0]]
    return resultados

if __name__ == "__main__":
    pregunta = "¿Dónde ocurre la fotosíntesis?"
    contexto = buscar_contexto(pregunta)
    for c in contexto:
        print("📄 Contexto relevante:", c)
