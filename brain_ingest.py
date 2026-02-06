import os
import glob
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Configuración
DATA_FOLDER = "ippsec_data"
DB_PATH = "ippsec_brain_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def ingest_data():
    print(f"[*] Inicializando IppSec Brain Ingestion...")
    
    # 1. Cargar documentos
    txt_files = glob.glob(os.path.join(DATA_FOLDER, "*.txt"))
    print(f"[*] Encontrados {len(txt_files)} archivos de transcripción.")
    
    documents = []
    for file_path in txt_files:
        try:
            loader = TextLoader(file_path, encoding='utf-8')
            documents.extend(loader.load())
        except Exception as e:
            print(f"[!] Error cargando {file_path}: {e}")

    print(f"[*] Total documentos cargados: {len(documents)}")

    # 2. Splitter (cortar en trozos manejables para el vector store)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        add_start_index=True
    )
    
    texts = text_splitter.split_documents(documents)
    print(f"[*] Total chunks generados: {len(texts)}")

    # 3. Embeddings y Vector Store
    print(f"[*] Generando embeddings con {EMBEDDING_MODEL} (esto puede tardar)...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    if os.path.exists(DB_PATH):
        print(f"[*] Base de datos existente encontrada en {DB_PATH}. Añadiendo datos...")
    else:
        print(f"[*] Creando nueva base de datos en {DB_PATH}...")

    # Crear/Actualizar DB
    # batch_size limita cuántos documentos se envían a la vez para evitar OOM
    batch_size = 166 
    total_batches = len(texts) // batch_size + 1
    
    vectorstore = Chroma(
        persist_directory=DB_PATH, 
        embedding_function=embeddings,
        collection_name="ippsec_brain"
    )

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        print(f"[*] Procesando batch {i // batch_size + 1}/{total_batches}...")
        vectorstore.add_documents(documents=batch)
        
    print("[*] Ingestión completada exitosamente.")

if __name__ == "__main__":
    ingest_data()
