# IppSec Brain (IaRAG) 

Sistema de RAG (Retrieval-Augmented Generation) avanzado que utiliza el razonamiento y conocimiento de los videos de **IppSec** y **S4vitar** para asistir en la resolución de máquinas y CTFs. 

## Características
- **Extracción Masiva**: Descarga y limpia automáticamente subtítulos de- **Multilingual Knowledge Base**: Indexed Transcripts from:
  - **IppSec** (English) - 900+ Videos.
  - **S4vitar** (Spanish) - 300+ Videos (including Live Streams).
- **Semantinc Search Engine**: Uses `paraphrase-multilingual-MiniLM-L12-v2` to understand queries in English or Spanish and find answers in any video.
- **MCP Integration**: Fully compatible with Claude/Gemini agents via Model Context Protocol.
- **Cross-Language Reasoning**: Ask in Spanish, get answers from IppSec's English content (and vice versa).l Context Protocol para integrar el conocimiento directamente en agentes como Antigravity o Gemini CLI.

### Usando el MCP (Desde tu Agente AI)

Una vez configurado en `mcp_config.json`:

1. "Explícame cómo IppSec hace la enumeración de Kerberos."
2. "Busca en los videos de S4vitar cómo resolver la máquina 'Forest'."
3. "¿Cómo se hace un buffer overflow básico? Busca en ambas fuentes."

## Estructura del Proyecto
- `ippsec_brain_harvester.py`: Script para recolectar transcripciones.
- `brain_ingest.py`: Procesa los textos y crea la base de datos vectorial.
- `brain_ask.py`: Interfaz de consulta con re-ranking.
- `ippsec_mcp_server.py`: Servidor para integración con herramientas externas.

## Uso Rapido
1. `python ippsec_brain_harvester.py` (Cosecha)
2. `python brain_ingest.py` (Ingestión)
3. `python brain_ask.py "pregunta"` (Consulta)
