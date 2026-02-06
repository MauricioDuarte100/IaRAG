import os
import glob
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Configuración
DATA_FOLDERS = ["ippsec_data", "s4vitar_data"]
DB_PATH = "ippsec_brain_db"
# Modelo multilingüe para mapear Inglés y Español al mismo espacio vectorial
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

def ingest_data():
    print(f"[*] Inicializando Brain Ingestion (Multilingüe)...")
    
    # 1. Cargar documentos de ambas fuentes
    documents = []
    for folder in DATA_FOLDERS:
        txt_files = glob.glob(os.path.join(folder, "*.txt"))
        print(f"[*] Carpeta '{folder}': {len(txt_files)} archivos encontrados.")
        
        for file_path in txt_files:
            try:
                # Añadimos metadatos para saber si es IppSec o S4vitar
                loader = TextLoader(file_path, encoding='utf-8')
                docs = loader.load()
                for doc in docs:
                    doc.metadata['source_type'] = folder
                documents.extend(docs)
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

    from tqdm import tqdm
    # Usamos tqdm para mostrar una barra de progreso visual
    for i in tqdm(range(0, len(texts), batch_size), desc="Ingestando Conocimiento", unit="batch"):
        batch = texts[i:i + batch_size]
        vectorstore.add_documents(documents=batch)
        
    print("[*] Ingestión completada exitosamente.")

if __name__ == "__main__":
    ingest_data()
