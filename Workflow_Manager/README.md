# Tarea: Workflow Managers - Introducción a Prefect

## ¿Qué es Prefect?
Basado en la charla "Task Failed Successfully" de Jeremiah Lowin (PyData Denver).

* **Definición:** Es un sistema de gestión de flujos de trabajo (*workflow manager*) diseñado para orquestar y monitorear tareas computacionales, asegurando que se ejecuten correctamente y manejando sus dependencias.
* **Ingeniería Positiva vs. Negativa:** Prefect distingue entre la "ingeniería positiva" (el código que realmente procesa datos y aporta valor) y la "ingeniería negativa" (la infraestructura, el manejo de errores, reintentos y dependencias). Su objetivo es gestionar toda la ingeniería negativa para que el desarrollador se enfoque en la lógica de negocio.
* **Fallar con Éxito:** A diferencia de otros sistemas que consideran los errores como anomalías catastróficas, Prefect trata el fallo como un estado normal y gestionable. Permite a los desarrolladores reaccionar ante los fallos y utilizarlos para dirigir el flujo del programa, evitando el "riesgo de sentido contrario" (*wrong-way risk*).
* **Integración:** Funciona de manera nativa con código Python estándar, utilizando decoradores (`@flow`, `@task`) para convertir funciones regulares en unidades de trabajo administradas por el sistema.

---

## Parte 1 y 2: Implementación y Modificación del Tutorial

Se desarrolló un flujo de trabajo (ETL) utilizando Prefect, modificando el ejemplo original para extraer, transformar y cargar datos desde una nueva fuente asignada: `https://jsonplaceholder.cypress.io/`.

### Código de Ejecución (`etl.py`)

```python
import requests 
from prefect import flow, task 

# Tarea 1: Extracción de datos con política de reintentos
@task(retries=3, retry_delay_seconds=2)
def obtener_usuarios():
    # URL asignada para la tarea
    url = "[https://jsonplaceholder.cypress.io/users](https://jsonplaceholder.cypress.io/users)"
    response = requests.get(url)
    response.raise_for_status() 
    return response.json()

# Tarea 2: Transformación de los datos
@task
def filtrar_nombres_emails(usuarios):
    # Procesamos la respuesta para extraer únicamente el nombre y el correo
    lista_procesada = [{"nombre": u["name"], "email": u["email"]} for u in usuarios]
    return lista_procesada

# Tarea 3: Carga/Muestra de resultados
@task
def mostrar_resultados(usuarios_procesados):
    print(f"Total de usuarios procesados exitosamente: {len(usuarios_procesados)}")
    for usuario in usuarios_procesados[:5]:  # Muestra los primeros 5 para simplificar
        print(f"- {usuario['nombre']} | {usuario['email']}")

# Flujo orquestador principal
@flow(log_prints=True)
def etl_cypress_users():
    print("Iniciando flujo ETL para jsonplaceholder.cypress.io")
    
    # El flujo pasa datos de una tarea a otra, gestionando las dependencias automáticamente
    datos_crudos = obtener_usuarios()
    datos_limpios = filtrar_nombres_emails(datos_crudos)
    mostrar_resultados(datos_limpios)

if __name__ == "__main__":
    etl_cypress_users()
```

---

## Resultados de Ejecución

Al ejecutar el script en la terminal (`python etl.py`), Prefect orquestó exitosamente el flujo. A continuación se presenta el registro de salida (log) y su explicación:

```text
PS C:\Users\Ezio0\Desktop\cosas fin\Computacion\workflow_manager> python etl.py
10:23:38.282 | INFO    | prefect - Starting temporary server on [http://127.0.0.1:8068](http://127.0.0.1:8068)
10:23:48.063 | INFO    | Flow run 'stereotyped-sunfish' - Beginning flow run 'stereotyped-sunfish' for flow 'etl-cypress-users'
10:23:48.071 | INFO    | Flow run 'stereotyped-sunfish' - Iniciando flujo ETL para jsonplaceholder.cypress.io
10:23:49.840 | INFO    | Task run 'obtener_usuarios-305' - Finished in state Completed()
10:23:49.858 | INFO    | Task run 'filtrar_nombres_emails-617' - Finished in state Completed()
10:23:49.869 | INFO    | Task run 'mostrar_resultados-4c3' - Total de usuarios procesados exitosamente: 10
10:23:49.872 | INFO    | Task run 'mostrar_resultados-4c3' - - Leanne Graham | Sincere@april.biz
10:23:49.874 | INFO    | Task run 'mostrar_resultados-4c3' - - Ervin Howell | Shanna@melissa.tv
10:23:49.875 | INFO    | Task run 'mostrar_resultados-4c3' - - Clementine Bauch | Nathan@yesenia.net
10:23:49.878 | INFO    | Task run 'mostrar_resultados-4c3' - - Patricia Lebsack | Julianne.OConner@kory.org
10:23:49.879 | INFO    | Task run 'mostrar_resultados-4c3' - - Chelsey Dietrich | Lucio_Hettinger@annie.ca
10:23:49.889 | INFO    | Task run 'mostrar_resultados-4c3' - Finished in state Completed()
10:23:49.983 | INFO    | Flow run 'stereotyped-sunfish' - Finished in state Completed()
10:23:50.047 | INFO    | prefect - Stopping temporary server on [http://127.0.0.1:8068](http://127.0.0.1:8068)
```

### Análisis de la Ejecución:
1. **Inicialización (`10:23:38`):** Prefect levanta un servidor temporal local para gestionar el estado y la base de datos de la ejecución.
2. **Orquestación del Flujo (`10:23:48`):** Inicia el flujo principal (`etl-cypress-users`) y le asigna un nombre de ejecución único (`stereotyped-sunfish`) para su trazabilidad.
3. **Ejecución de Tareas y Dependencias (`10:23:49`):** * La tarea de extracción (`obtener_usuarios`) se conecta a la API y finaliza con estado `Completed()`.
   * Inmediatamente después, se ejecuta la transformación (`filtrar_nombres_emails`), validando que Prefect manejó correctamente la dependencia de datos entre ambas tareas.
4. **Resultados (`10:23:49`):** La tarea final (`mostrar_resultados`) imprime correctamente los datos transformados (nombres y correos) capturados desde la API.
5. **Cierre (`10:23:50`):** El flujo completo se marca como exitoso (`Completed()`) y el servidor temporal se apaga para liberar recursos.