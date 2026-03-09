import subprocess
import time
import random
import os

def simular_usuario_n():
    print("Chaos Monkey (Usuario N) ha entrado al sistema...")
    
    espera = random.randint(1, 3)
    print(f"Esperando {espera} segundos...")
    time.sleep(espera)

    print("Buscando la identidad de 'app.py'...")

    # Leemos el archivo donde la app dejó su identificación
    if os.path.exists('app.pid'):
        with open('app.pid', 'r') as f:
            pid = f.read().strip()
            
        print(f"¡Proceso encontrado! PID: {pid}. Ejecutando orden de cierre...")
        
        # Comando infalible de Windows para matar el PID específico
        resultado = subprocess.run(f"taskkill /F /PID {pid}", shell=True, capture_output=True, text=True)
        
        if "CORRECTO" in resultado.stdout or "SUCCESS" in resultado.stdout:
            print("El programa fue cerrado agresivamente por el usuario.")
            print("Revisa tu terminal izquierda para ver la recuperación.")
        else:
            print("El proceso ya no existía (probablemente falló por sí solo justo antes).")
    else:
        print("No encontré el archivo 'app.pid'.")

if __name__ == "__main__":
    simular_usuario_n()