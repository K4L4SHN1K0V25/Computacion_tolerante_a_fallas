import requests # Libreria estandar para hacer peticiones HTTP a APIs web.
from prefect import flow, task # Importamos los decoradores principales de Prefect para orquestar.

# El decorador @task define una unidad de trabajo aislada. 
# retries=2 le indica a Prefect que reintente la ejecucion hasta 2 veces si falla (ej. error de red).
@task(retries=2)
def extraer_datos():
    # Definimos la URL de la API publica de prueba de donde obtendremos los datos.
    url = "https://jsonplaceholder.typicode.com/posts/1"
    # Realizamos una peticion GET a la URL.
    response = requests.get(url)
    # Parseamos la respuesta de la API de formato JSON a un diccionario de Python.
    return response.json()

# Otro decorador @task. Esta tarea depende de los datos que reciba como argumento.
@task
def transformar_datos(datos):
    # Buscamos la clave "title" en el diccionario recibido. 
    # Si no existe, usamos "Sin titulo" por defecto. Finalmente, convertimos el texto a MAYuSCULAS.
    return datos.get("title", "Sin titulo").upper()

# El decorador @flow define el flujo principal que orquesta las tareas.
# log_prints=True asegura que los prints estandar de Python se registren en el sistema de logs de Prefect.
@flow(log_prints=True)
def mi_primer_flujo():
    # Mensaje inicial registrado en los logs del flujo.
    print("Iniciando flujo de trabajo en Prefect...")
    
    # Ejecutamos la primera tarea. Prefect gestionara su estado (exito/fallo/reintentos).
    datos_crudos = extraer_datos()
    
    # Ejecutamos la segunda tarea pasandole el resultado de la primera.
    # Prefect infiere automaticamente que transformar_datos depende de extraer_datos.
    resultado = transformar_datos(datos_crudos)
    
    # Imprimimos el resultado final procesado en los logs.
    print(f"Resultado procesado: {resultado}")

# Bloque estandar de Python para asegurar que el codigo solo se ejecute 
# si el script se corre directamente desde la terminal (ej. python tutorial.py).
if __name__ == "__main__":
    mi_primer_flujo() # Iniciamos la ejecucion del flujo orquestador.