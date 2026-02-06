# IppSec Brain (IaRAG) 🧠

Sistema de RAG (Retrieval-Augmented Generation) avanzado que utiliza el razonamiento y conocimiento de los videos de **IppSec** para asistir en la resolución de máquinas y CTFs.

## Características
- **Extracción Masiva**: Descarga y limpia automáticamente subtítulos de todo el canal de IppSec.
- **RAG Modo Elite**: Implementa búsqueda vectorial con ChromaDB y re-ranking mediante Cross-Encoders para máxima precisión.
- **Integración MCP**: Servidor compatible con Model Context Protocol para integrar el conocimiento directamente en agentes como Antigravity o Gemini CLI.

## Estructura del Proyecto
- `ippsec_brain_harvester.py`: Script para recolectar transcripciones.
- `brain_ingest.py`: Procesa los textos y crea la base de datos vectorial.
- `brain_ask.py`: Interfaz de consulta con re-ranking.
- `ippsec_mcp_server.py`: Servidor para integración con herramientas externas.

## Uso Rapido
1. `python ippsec_brain_harvester.py` (Cosecha)
2. `python brain_ingest.py` (Ingestión)
3. `python brain_ask.py "pregunta"` (Consulta)
