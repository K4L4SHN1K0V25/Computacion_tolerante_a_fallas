# Workflow de Clasificación de Correos con IA (Tolerante a Fallos)

Este flujo de n8n automatiza la clasificación de correos electrónicos utilizando modelos de lenguaje (LLM). Ha sido diseñado bajo principios de ingeniería de software para garantizar la continuidad del proceso incluso ante fallos de API o formatos inesperados.

## 🛠 Arquitectura de Robustez

El sistema implementa cinco capas de protección para evitar detenciones inesperadas:

### 1. Validación Dinámica de Datos (Capa Lógica)
Se utiliza un nodo **Code (JavaScript)** entre la IA y la toma de decisiones para normalizar las respuestas. 
- **Función:** Convierte respuestas ambiguas de la IA en valores booleanos estrictos (`isTarget: true/false`).
- **Seguridad:** Si la IA devuelve un formato erróneo o vacío, el código lo captura y lo clasifica por defecto como `Otro`, evitando que el nodo `If` falle por datos nulos.

### 2. Control de Flujo y Cadencia (Capa de Persistencia)
Para evitar la saturación de las APIs y garantizar que cada correo se procese correctamente sin perder el progreso:

* **Nodo Loop Over Items:** Implementamos una estructura de iteración que garantiza el procesamiento secuencial. Esto evita que el servidor intente procesar cientos de correos en paralelo, lo que causaría fallos de memoria o bloqueos de cuenta.
* **Nodo Wait (Control de Throttle):** Se ha integrado una pausa estratégica dentro del bucle. Esto regula la cadencia de peticiones hacia Gemini y Gmail, respetando los límites de velocidad (Rate Limits) y permitiendo que las conexiones se liberen antes de la siguiente iteración.
* **Recuperación de Progreso:** Al trabajar con un loop controlado por lotes, si el flujo se detiene, el sistema permite identificar fácilmente en qué punto de la lista se quedó la ejecución, facilitando el reintento manual o automático desde el último ítem válido.

### 3. Política de Reintentos (Capa de Red)
Los nodos críticos (**Gmail** y **Message a model**) tienen configurada la política de reintentos:
- **Max Retries:** 3
- **Intervalo:** 5 segundos
- Esto soluciona errores de red temporales o micro-caídas de las APIs de Google y Gemini.

### 4. Modo "Continue on Fail" (Aislamiento de Errores)
El nodo de la IA tiene activada la opción **Continue on Fail**. 
- **Beneficio:** Si un correo específico causa un error de seguridad (Filtros de contenido) o cuota en la IA, el loop NO se detiene. El flujo marca ese ítem como fallido y continúa con el siguiente correo de la lista.

### 5. Sistema de Alerta Global (Error Trigger)
El workflow está vinculado a un **Error Workflow** independiente.
- **Disparador:** Nodo `Error Trigger`.
- **Acción:** Notificación automática en caso de fallo crítico no recuperable.
- **Observabilidad:** Envía detalles técnicos (nombre del nodo, mensaje de error y ID de ejecución) para un debug rápido.

## 🚀 Configuración del Nodo de Clasificación (JS)

```javascript
for (const item of $input.all()) {
  const aiResponse = (item.json.message?.text || "").toLowerCase();
  
  if (aiResponse.includes('linkedin')) {
    item.json.category = "LinkedIn";
    item.json.isTarget = true;
  } else {
    item.json.category = "Otro";
    item.json.isTarget = false;
  }
}
return $input.all();
```

## 📋 Requisitos para Mantenimiento

* **Etiquetas en Gmail:** Asegurarse de que existan las etiquetas `Procesando` y `IA_Procesado` en la cuenta de correo vinculada.
* **API Quotas:** Monitorear el uso de tokens y límites de velocidad en **Google Cloud Console** y el panel de la IA para evitar errores **429** (*Too Many Requests*).
* **Error Workflow:** Mantener activo y vinculado el flujo de notificaciones para asegurar una **supervisión pasiva** y reaccionar rápido ante incidentes.