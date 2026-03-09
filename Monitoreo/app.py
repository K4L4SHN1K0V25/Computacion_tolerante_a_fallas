import time
import random
import logging
import sys
import os

# Configuracion del registro persistente
logging.basicConfig(
    filename='app_principal.log', 
    level=logging.INFO,
    format='%(asctime)s - PROCESO A - %(levelname)s - %(message)s'
)

ARCHIVO_ESTADO = 'estado.txt'

def leer_estado():
    """Intenta recuperar el ciclo donde se quedo la app."""
    if os.path.exists(ARCHIVO_ESTADO):
        try:
            with open(ARCHIVO_ESTADO, 'r') as f:
                estado_anterior = int(f.read().strip())
                nuevo_ciclo = estado_anterior + 1
                logging.info(f"Estado recuperado con exito. Reanudando desde el ciclo {nuevo_ciclo}.")
                print(f"Proceso A: ¡Recupere mi memoria! Continuando en el ciclo {nuevo_ciclo}...")
                return nuevo_ciclo
        except ValueError:
            # Escenario 2: El archivo existe pero esta corrupto (no es un numero)
            logging.warning("Archivo de estado corrupto o ilegible. No se pudo recuperar el progreso.")
            print("Proceso A: Mi memoria esta corrupta. Iniciando desde cero por seguridad...")
            return 0
    return 0 # Si no existe el archivo, empezamos de 0

def guardar_estado(ciclo):
    """Guarda el ciclo actual en el disco."""
    with open(ARCHIVO_ESTADO, 'w') as f:
        f.write(str(ciclo))

def corromper_estado():
    """Simula una falla catastrofica donde el archivo se daña al escribir."""
    with open(ARCHIVO_ESTADO, 'w') as f:
        f.write("DATOS_CORRUPTOS_ERROR_0x883")

def ejecutar_servicio():
    logging.info("Iniciando servicio principal...")
    
    # Intentamos recuperar el estado al arrancar
    ciclos = leer_estado()
    
    while True:
        logging.info(f"Procesando lote de datos #{ciclos}...")
        print(f"Procesando lote #{ciclos}...")
        
        # Guardamos el estado ANTES de procesar para asegurar que sabemos donde estamos
        guardar_estado(ciclos)
        time.sleep(2) # Simula tiempo de procesamiento
        
        # Simulador de fallas (Tiramos un dado del 1 al 10)
        dado = random.randint(1, 10)
        
        if dado == 9:
            # ESCENARIO 1: Falla normal. El proceso muere pero el estado quedo bien guardado.
            logging.error("¡Falla critica del sistema! El proceso murio inesperadamente.")
            print("Proceso A: ¡Me he caido (Falla Normal)!")
            sys.exit(1)
            
        elif dado == 10:
            # ESCENARIO 2: Falla catastrofica. Se corrompe el disco/archivo justo al fallar.
            logging.error("¡Falla catastrofica! El proceso murio y el archivo de estado se daño.")
            print("Proceso A: ¡Me he caido y mi archivo se daño (Falla Catastrofica)!")
            corromper_estado()
            sys.exit(1)
            
        ciclos += 1

if __name__ == "__main__":
    ejecutar_servicio()