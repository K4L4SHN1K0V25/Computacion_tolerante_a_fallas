# Sistema Tolerante a Fallas: Patrón Monitor (Watchdog) con Recuperación de Estado

Este proyecto implementa un sistema robusto de tolerancia a fallas utilizando dos procesos independientes en Python. Demuestra la orquestación de subprocesos, el monitoreo continuo, el manejo de señales del sistema operativo y estrategias avanzadas de recuperación de estado.



## Propuesta del Escenario

**1. El problema a resolver:**
Se requiere asegurar la alta disponibilidad de un servicio principal (**Proceso A**) encargado de procesar lotes de datos secuenciales. Este servicio es crítico y no puede permitirse tiempos prolongados de inactividad. Además, si el servicio cae, debe ser capaz de recordar en qué lote se quedó para no repetir trabajo, o bien, iniciar desde cero si su memoria se corrompe. Para lograr esto, se implementó un proceso monitor (**Demonio B**) que vigila su salud de manera ininterrumpida.

**2. Por qué requiere ejecución en segundo plano:**
El servicio de procesamiento y su monitor están diseñados para operar 24/7 en un servidor sin requerir interacción humana (funcionamiento *headless*). Al ejecutarse como un demonio en segundo plano, el sistema opera de forma silenciosa, supervisando el entorno sin bloquear la terminal del usuario y sobreviviendo a cierres de sesión.

**3. Qué tipo de fallas podrían ocurrir:**
El Proceso A simula escenarios reales de falla en producción:
* **Falla Normal (Escenario 1):** El proceso muere por una excepción (ej. pérdida de conexión a BD), pero logra guardar su último estado válido.
* **Falla Catastrófica (Escenario 2):** El proceso muere y el archivo de persistencia en disco (`estado.txt`) se corrompe, simulando un fallo de hardware o un error fatal de escritura.
* **Interrupciones del Usuario:** El usuario o administrador del sistema envía una señal de apagado manual (`SIGINT` mediante `Ctrl+C`).

**4. Estrategia de tolerancia aplicada:**
Se aplicó el patrón de diseño **Monitor / Watchdog** con **Separación de Responsabilidades**:
* **Monitoreo Continuo:** El **Demonio B** (`monitor.py`) ejecuta el **Proceso A** (`app.py`) mediante el módulo `subprocess` y se queda a la escucha de su estado con `.wait()`.
* **Recuperación Automática:** Si el Proceso A se cierra con un código de error, el Demonio B lo detecta, registra la alerta en el log y reinicia el servicio automáticamente.
* **Manejo de Estado (Stateful vs Stateless):** Al reiniciar, el Proceso A lee el archivo `estado.txt`. Si es válido, reanuda el trabajo exactamente donde se quedó. Si está corrupto, atrapa la excepción y reinicia el conteo desde cero por seguridad.
* **Registro Persistente:** Ambos procesos utilizan la librería `logging` para escribir historiales detallados en `monitor_sistema.log` y `app_principal.log`.
* **Manejo de Señales:** El Demonio B intercepta la señal `KeyboardInterrupt` para apagar el sistema de monitoreo de forma limpia y controlada, evitando procesos "zombies".

---

## Instrucciones de Ejecución

1.  Asegúrate de tener Python 3 instalado en tu sistema.
2.  Coloca `app.py` y `monitor.py` en el mismo directorio.
3.  Abre una terminal en esa ruta y ejecuta únicamente el monitor:
    ```bash
    python monitor.py
    ```
4.  **Observación:** Observa la salida en la consola. Verás cómo la aplicación procesa lotes y guarda su progreso.
5.  **Simulación de Fallas:** El sistema fallará aleatoriamente. Notarás cómo el monitor detecta la caída y reinicia la app. Podrás ver en consola si la app logró recuperar su estado anterior o si tuvo que iniciar desde cero por corrupción de datos.
6.  **Cierre Seguro:** Presiona `Ctrl + C` en la terminal. Verás que el monitor atrapa la señal y se detiene correctamente.
7.  **Auditoría:** Revisa los archivos `app_principal.log`, `monitor_sistema.log` y `estado.txt` generados en la carpeta para auditar el comportamiento del sistema.