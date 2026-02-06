import sys
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Configuración (debe coincidir con ingest.py)
DB_PATH = "ippsec_brain_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

from sentence_transformers import CrossEncoder

def ask_brain(query, return_results=False):
    print(f"[*] Cargando IppSec Brain (Modo Elite: Re-ranking Activado)...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    vectorstore = Chroma(
        persist_directory=DB_PATH, 
        embedding_function=embeddings,
        collection_name="ippsec_brain"
    )

    # 1. Recuperación Inicial (Broad Search)
    print(f"[*] Recuperando candidatos para: '{query}'...")
    # Recuperamos más resultados de lo normal (k=20) para que el re-ranker filtre
    initial_results = vectorstore.similarity_search(query, k=20)
    
    # 2. Re-ranking (Fine-grained Search)
    # Usamos un modelo Cross-Encoder pre-entrenado para MS MARCO (bueno para Q&A)
    reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    
    # Preparamos pares [query, contenido] para el modelo
    predict_inputs = [[query, doc.page_content] for doc in initial_results]
    scores = reranker.predict(predict_inputs)
    
    # Ordenamos por score descendente
    ranked_results = sorted(zip(scores, initial_results), key=lambda x: x[0], reverse=True)
    
    # Nos quedamos con los Top 5 mejores
    top_results = ranked_results[:5]

    if return_results:
        return [doc for score, doc in top_results]

    print(f"\n{'='*50}")
    print(f"TOP RESULTADOS DE IPPSEC (Re-ranked)")
    print(f"{'='*50}\n")
    
    for i, (score, doc) in enumerate(top_results):
        source = doc.metadata.get('source', 'Desconocido')
        content = doc.page_content
        print(f"--- Resultado {i+1} (Score: {score:.4f}) (Fuente: {source}) ---")
        print(f"{content}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python brain_ask.py \"Tu pregunta sobre CTF\"")
        sys.exit(1)
    
    query = sys.argv[1]
    ask_brain(query)
