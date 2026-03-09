import subprocess
import time
import logging

# Configuracion del registro persistente (Log) para el Monitor
logging.basicConfig(
    filename='monitor_sistema.log', 
    level=logging.INFO,
    format='%(asctime)s - DEMONIO - %(levelname)s - %(message)s'
)

def iniciar_demonio():
    logging.info("Demonio iniciado. Monitoreo activado.")
    print("Demonio de monitoreo ejecutandose en segundo plano (presiona Ctrl+C para detener)...")
    
    while True:
        logging.info("Arrancando el Proceso A (app.py)...")
        
        # Ejecutamos el Proceso A como un subproceso independiente
        proceso_a = subprocess.Popen(["python", "app.py"])
        
        # El demonio espera aqui hasta que el proceso_a termine o muera
        proceso_a.wait()
        
        # Evaluamos por que termino el proceso
        if proceso_a.returncode != 0:
            mensaje_falla = f"El Proceso A murio inesperadamente (Codigo de salida: {proceso_a.returncode})."
            logging.warning(mensaje_falla)
            print(f"ALERTA: {mensaje_falla}")
            
            logging.info("Aplicando tolerancia a fallas: Reiniciando el servicio en 3 segundos...")
            time.sleep(3) # Pausa de seguridad antes del reinicio
        else:
            # Si por alguna razon termina de forma "limpia" (codigo 0), lo volvemos a levantar
            logging.info("El Proceso A termino de forma natural. Reiniciando por politica 24/7...")
            time.sleep(3)

if __name__ == "__main__":
    try:
        iniciar_demonio()
    except KeyboardInterrupt:
        logging.info("Demonio de monitoreo detenido manualmente por el usuario.")
        print("\nMonitor detenido.")