import time
import random
import logging
import sys
import os

logging.basicConfig(
    filename='app_principal.log', 
    level=logging.INFO,
    format='%(asctime)s - PROCESO A - %(levelname)s - %(message)s'
)

ARCHIVO_ESTADO = 'estado.txt'
ARCHIVO_PID = 'app.pid' # Nuevo archivo para guardar la identidad del proceso

def registrar_pid():
    """Guarda el ID del proceso a nivel de Sistema Operativo."""
    with open(ARCHIVO_PID, 'w') as f:
        f.write(str(os.getpid()))

def leer_estado():
    if os.path.exists(ARCHIVO_ESTADO):
        try:
            with open(ARCHIVO_ESTADO, 'r') as f:
                estado_anterior = int(f.read().strip())
                nuevo_ciclo = estado_anterior + 1
                logging.info(f"Estado recuperado con axito. Reanudando desde el ciclo {nuevo_ciclo}.")
                print(f"Proceso A: ¡Recupera mi memoria! Continuando en el ciclo {nuevo_ciclo}...")
                return nuevo_ciclo
        except ValueError:
            logging.warning("Archivo de estado corrupto o ilegible.")
            print("Proceso A: Mi memoria esta corrupta. Iniciando desde cero por seguridad...")
            return 0
    return 0 

def guardar_estado(ciclo):
    with open(ARCHIVO_ESTADO, 'w') as f:
        f.write(str(ciclo))

def corromper_estado():
    with open(ARCHIVO_ESTADO, 'w') as f:
        f.write("DATOS_CORRUPTOS_ERROR_0x883")

def ejecutar_servicio():
    registrar_pid() # <--- Registramos el PID al arrancar
    logging.info("Iniciando servicio principal...")
    
    ciclos = leer_estado()
    
    while True:
        print(f"Procesando lote #{ciclos}...")
        guardar_estado(ciclos)
        time.sleep(2) 
        
        dado = random.randint(1, 20)
        
        if dado == 19:
            print("Proceso A: ¡Me he caido (Falla Normal)!")
            sys.exit(1)
        elif dado == 20:
            print("Proceso A: ¡Me he caido y mi archivo se daño (Falla Catastrofica)!")
            corromper_estado()
            sys.exit(1)
            
        ciclos += 1

if __name__ == "__main__":
    ejecutar_servicio()