import os
import glob
from collections import deque

def limpiar_y_consolidar(output_folder):
    print("[*] Limpiando archivos SRT y convirtiendo a texto plano (Test Mode - Deque)...")
    
    archivos_srt = glob.glob(os.path.join(output_folder, "*.srt"))
    
    if not archivos_srt:
        print("No srt files found")
        return

    for archivo in archivos_srt:
        nombre_base = os.path.splitext(archivo)[0]
        archivo_txt = f"{nombre_base}.txt"
        
        # Always overwrite in this test mode to verify fix
        
        print(f"Processing {archivo}...")
        try:
            with open(archivo, 'r', encoding='utf-8') as f_in, \
                 open(archivo_txt, 'w', encoding='utf-8') as f_out:
                
                lines = f_in.readlines()
                seen_window = deque(maxlen=5)
                
                for line in lines:
                    # Filtrar marcas de tiempo, números de secuencia y líneas vacías
                    if '-->' in line or line.strip().isdigit() or not line.strip():
                        continue
                    
                    # Limpieza básica
                    clean_line = line.strip()
                    
                    # Evitar duplicados si la línea está en la ventana reciente
                    if clean_line not in seen_window:
                        f_out.write(clean_line + " ")
                        seen_window.append(clean_line)
                        
            print(f"[+] Procesado: {os.path.basename(archivo_txt)}")
        except Exception as e:
            print(f"Error processing {archivo}: {e}")

if __name__ == "__main__":
    limpiar_y_consolidar("ippsec_data")
