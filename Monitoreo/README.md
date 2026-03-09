# Sistema Tolerante a Fallas: Patrón Monitor (Watchdog), Recuperación de Estado e Ingeniería del Caos

Este proyecto implementa un sistema robusto de tolerancia a fallas centrado en la orquestación de subprocesos, el monitoreo continuo, la recuperación de estado y las pruebas de resiliencia automatizadas (Chaos Engineering) mediante dos procesos independientes en Python.

## Propuesta del Escenario

**1. El problema a resolver:**
Se requiere asegurar la alta disponibilidad de un servicio principal (**Proceso A**) enfocado en procesar lotes de datos secuenciales. Este servicio es crítico y no puede permitirse tiempos prolongados de inactividad. Además, si el servicio cae, debe ser capaz de recordar en qué lote se quedó para no repetir trabajo, o bien, iniciar desde cero si su memoria se corrompe. Para lograr esto, se implementó un proceso monitor (**Demonio B**) que vigila su salud de manera ininterrumpida.

**2. Por qué requiere ejecución en segundo plano:**
El servicio de procesamiento y su monitor están diseñados para operar 24/7 en un servidor sin requerir interacción humana (funcionamiento *headless*). Al ejecutarse como un demonio en segundo plano, el sistema opera de forma silenciosa, supervisando el entorno sin bloquear la terminal del usuario y sobreviviendo a cierres de sesión.

**3. Qué tipo de fallas podrían ocurrir:**
El Proceso A simula escenarios reales de falla en producción:
* **Falla Normal (Escenario 1):** El proceso muere por una excepción (ej. pérdida de conexión a BD), pero logra guardar su último estado válido.
* **Falla Catastrófica (Escenario 2):** El proceso muere y el archivo de persistencia en disco (`estado.txt`) se corrompe, simulando un fallo de hardware o un error fatal de escritura.
* **Intervención Externa (Usuario N / Chaos Monkey):** Un usuario o un administrador del sistema cierra el proceso abruptamente desde el Administrador de Tareas.

**4. Estrategia de tolerancia aplicada:**
Se aplicó el patrón de diseño **Monitor / Watchdog** con **Separación de Responsabilidades**:
* **Monitoreo Continuo:** El **Demonio B** (`monitor.py`) ejecuta el **Proceso A** (`app.py`) mediante el módulo `subprocess` y se queda a la escucha de su estado con `.wait()`.
* **Manejo de Identidad (Archivos PID):** El Proceso A registra su ID de proceso del sistema operativo en un archivo físico (`app.pid`) al arrancar. Esto es un estándar de la industria que permite identificar y administrar el proceso de forma inequívoca.
* **Recuperación Automática:** Si el Proceso A se cierra con un código de error, el Demonio B lo detecta de inmediato, registra la alerta en el log y reinicia el servicio.
* **Manejo de Estado (Stateful vs Stateless):** Al reiniciar, el Proceso A lee el archivo `estado.txt`. Si es válido, reanuda el trabajo exactamente donde se quedó. Si está corrupto, atrapa la excepción y reinicia el conteo desde cero.
* **Registro Persistente:** Ambos procesos utilizan la librería `logging` para escribir historiales detallados en `monitor_sistema.log` y `app_principal.log`.
* **Manejo de Señales:** El Demonio B intercepta la señal `KeyboardInterrupt` para apagar el sistema de forma controlada.

---

## Instrucciones de Ejecución y Pruebas de Resiliencia

### Fase 1: Arranque y Monitoreo
1.  Asegúrate de tener Python instalado en tu sistema.
2.  Coloca `app.py`, `monitor.py` y `chaos_monkey.py` en el mismo directorio.
3.  Abre una terminal en esa ruta y ejecuta el monitor:
    ```bash
    python monitor.py
    ```
4.  Observa cómo la aplicación procesa lotes y cómo el monitor la reinicia automáticamente cuando simula fallas internas.

### Fase 2: Prueba de Ingeniería del Caos (Simulación Usuario N)
Para comprobar que el sistema sobrevive a cierres abruptos externos:
1.  Mantén el monitor corriendo en tu **Terminal 1**.
2.  Abre una **Terminal 2** en la misma ruta del proyecto.
3.  Ejecuta el script de prueba:
    ```bash
    python chaos_monkey.py
    ```
4.  Este script leerá el archivo `app.pid` y enviará una señal de finalización (`SIGKILL`/`taskkill`) directo a la aplicación.
5.  Observa en la Terminal 1 cómo el monitor detecta el ataque exitosamente, registra la caída no planificada y levanta el servicio de nuevo en cuestión de segundos, demostrando resiliencia total.

### Auditoría
Revisa los archivos `app_principal.log`, `monitor_sistema.log` y `estado.txt` generados en la carpeta para auditar el historial de eventos, fallas y recuperaciones del sistema.