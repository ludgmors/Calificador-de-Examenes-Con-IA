from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

modelo = SentenceTransformer('all-MiniLM-L6-v2')

def crear_indice_vectorial(documentos, nombre_indice='indice_faiss'):
    # documentos: lista de strings (textos)
    embeddings = modelo.encode(documentos, convert_to_numpy=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    # Guardar índice y textos originales
    faiss.write_index(index, f"{nombre_indice}.index")
    with open(f"{nombre_indice}_documentos.pkl", "wb") as f:
        pickle.dump(documentos, f)
    
    print("✅ Índice FAISS y documentos guardados.")

if __name__ == "__main__":
    documentos = [
        "El agua hierve a 100 grados.",
        "La fotosíntesis ocurre en las hojas de las plantas.",
        "La independencia de América fue un proceso largo y complejo."
    ]
    crear_indice_vectorial(documentos)
