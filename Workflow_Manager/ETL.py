import requests
from prefect import flow, task

# Tarea 1: Extracción con política de reintentos
@task(retries=3, retry_delay_seconds=2)
def obtener_usuarios():
    # Utilizando la nueva URL asignada en tu tarea
    url = "https://jsonplaceholder.cypress.io/users"
    response = requests.get(url)
    response.raise_for_status() 
    return response.json()

# Tarea 2: Transformación de los datos
@task
def filtrar_nombres_emails(usuarios):
    # Procesamos la respuesta para extraer únicamente el nombre y el correo
    lista_procesada = [{"nombre": u["name"], "email": u["email"]} for u in usuarios]
    return lista_procesada

# Tarea 3: Acción final o carga
@task
def mostrar_resultados(usuarios_procesados):
    print(f"Total de usuarios procesados exitosamente: {len(usuarios_procesados)}")
    for usuario in usuarios_procesados[:5]:  # Muestra los primeros 5 para simplificar
        print(f"- {usuario['nombre']} | {usuario['email']}")

# Flujo orquestador principal
@flow(log_prints=True)
def etl_cypress_users():
    print("Iniciando flujo ETL para jsonplaceholder.cypress.io")
    
    # El flujo pasa datos de una tarea a otra naturalmente (Ingeniería Positiva pura)
    datos_crudos = obtener_usuarios()
    datos_limpios = filtrar_nombres_emails(datos_crudos)
    mostrar_resultados(datos_limpios)

if __name__ == "__main__":
    etl_cypress_users()