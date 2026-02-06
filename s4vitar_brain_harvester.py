import os
import subprocess
import glob
from collections import deque

# Descargamos playlists específicas curadas por el usuario (HTB y VulnHub)
CHANNEL_URLS = [
    "https://www.youtube.com/playlist?list=PLWys0ZbXYUy4x2gR3LFDa0bZw4OZ1m8k-", # Playlist 1
    "https://www.youtube.com/playlist?list=PLWys0ZbXYUy7GYspoUPPsGzCu1bdgUdzf"  # Playlist 2
]
OUTPUT_FOLDER = "s4vitar_data"

# Palabras clave para filtrar solo contenido técnico de resolución de máquinas
KEYWORDS = [
    "HackTheBox", "HTB", "VulnHub", "OSCP", "Machine", "Máquina", "CTF", 
    "Walkthrough", "Resolución", "Writeup", "Privilege Escalation", 
    "Buffer Overflow", "Active Directory"
]

def descargar_transcripciones_s4vitar():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    
    print(f"[*] Iniciando cosecha selectiva de S4vitar (S4viSinFiltro)...")
    print(f"[*] Filtros activos: {KEYWORDS}")

    # Usamos match-filter de yt-dlp para descargar solo lo que nos interesa
    # Construimos una regex gigante: (?i)(keyword1|keyword2|...)
    regex_filter = "(?i)(" + "|".join(KEYWORDS) + ")"
    print(f"[*] Regex de filtrado: {regex_filter}")

    import sys
    
    for url in CHANNEL_URLS:
        print(f"[*] Procesando fuente: {url}")
        command = [
            sys.executable, "-m", "yt_dlp",
            "--write-auto-sub",
            "--sub-lang", "es",  # Español
            "--skip-download",
            "--convert-subs", "srt",
            "--match-filter", f"title ~= '{regex_filter}'",
            "--output", f"{OUTPUT_FOLDER}/%(title)s.%(ext)s",
            url
        ]

        try:
            subprocess.run(command)
        except Exception as e:
            print(f"[!] Error ejecutando yt-dlp para {url}: {e}")
            
    print("[*] Descarga de subtítulos de S4vitar completada.")

def limpiar_y_consolidar():
    print("[*] Limpiando archivos SRT y convirtiendo a texto plano (S4vitar)...")
    
    archivos_srt = glob.glob(os.path.join(OUTPUT_FOLDER, "*.srt"))
    
    for archivo in archivos_srt:
        nombre_base = os.path.splitext(archivo)[0]
        archivo_txt = f"{nombre_base}.txt"
        
        # Si ya existe el txt, saltamos (idempotencia)
        if os.path.exists(archivo_txt):
            continue
            
        try:
            with open(archivo, 'r', encoding='utf-8') as f_in, \
                 open(archivo_txt, 'w', encoding='utf-8') as f_out:
                
                lines = f_in.readlines()
                # Deque para deduplicación (Sliding Window)
                seen_window = deque(maxlen=10)
                
                for line in lines:
                    if '-->' in line or line.strip().isdigit() or not line.strip():
                        continue
                    
                    clean_line = line.strip()
                    
                    # Deduplicación agresiva
                    if clean_line not in seen_window:
                        f_out.write(clean_line + " ")
                        seen_window.append(clean_line)
                        
            # Eliminar el .srt original para ahorrar espacio/ruido (opcional)
            # os.remove(archivo) 
            
        except Exception as e:
            print(f"[!] Error procesando {archivo}: {e}")

    print("[*] Limpieza finalizada.")

if __name__ == "__main__":
    descargar_transcripciones_s4vitar()
    limpiar_y_consolidar()
