import os
import subprocess
import glob

def descargar_transcripciones(channel_url, output_folder="ippsec_data"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    print(f"[*] Iniciando descarga de subtítulos para: {channel_url}")
    print("[*] Esto puede tomar unos minutos dependiendo de la cantidad de videos...")

    # Comando base de yt-dlp
    # --write-auto-sub: Descarga subtítulos generados automáticamente si no hay manuales
    # --sub-lang en: Prefiere inglés
    # --skip-download: NO descarga el video (ahorra espacio y tiempo)
    # --convert-subs srt: Convierte a formato SRT estándar
    # Usar sys.executable para llamar a yt-dlp como módulo y evitar problemas de PATH
    import sys
    command = [
        sys.executable, "-m", "yt_dlp",
        "--write-auto-sub",
        "--sub-lang", "en",
        "--skip-download",
        "--convert-subs", "srt",
        "--output", f"{output_folder}/%(title)s.%(ext)s",
        channel_url
    ]

    try:
        subprocess.run(command, check=True)
        print("[*] Descarga de subtítulos completada.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error ejecutando yt-dlp: {e}")

def limpiar_y_consolidar(output_folder):
    print("[*] Limpiando archivos SRT y convirtiendo a texto plano...")
    
    archivos_srt = glob.glob(os.path.join(output_folder, "*.srt"))
    
    for archivo in archivos_srt:
        nombre_base = os.path.splitext(archivo)[0]
        archivo_txt = f"{nombre_base}.txt"
        
        with open(archivo, 'r', encoding='utf-8') as f_in, \
             open(archivo_txt, 'w', encoding='utf-8') as f_out:
            
            lines = f_in.readlines()
            from collections import deque
            # Mantener un historial de las últimas líneas para evitar duplicados inmediatos
            seen_window = deque(maxlen=10)
            
            for line in lines:
                # Filtrar marcas de tiempo, números de secuencia y líneas vacías
                if '-->' in line or line.strip().isdigit() or not line.strip():
                    continue
                
                # Limpieza básica de etiquetas HTML o formato residual
                clean_line = line.strip()
                
                # Evitar duplicados si la línea está en la ventana reciente
                if clean_line not in seen_window:
                    f_out.write(clean_line + " ")
                    seen_window.append(clean_line)

        # Opcional: Eliminar el SRT original para ahorrar espacio
        # os.remove(archivo)
        print(f"[+] Procesado: {os.path.basename(archivo_txt)}")

if __name__ == "__main__":
    # URL del canal de IppSec (o lista de reproducción "Machines")
    IPPSEC_URL = "https://www.youtube.com/@IppSec/videos" 
    
    descargar_transcripciones(IPPSEC_URL)
    limpiar_y_consolidar("ippsec_data")
