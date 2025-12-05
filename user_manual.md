# Manual de Usuario del Robot T4: Operación Autónoma y Programación

## 1. Introducción al Robot T4

¡Bienvenido al Proyecto T4! Su robot es un autómata de producción, diseñado para la autonomía total en el hogar. Utiliza un **Cerebro Integrado** (basado en la arquitectura MindOn) y comunicación de largo alcance **LoRaWAN** para un control seguro y *offline*.

## 2. Interacción Humano-Robot (HRI)

El robot T4 está diseñado para responder a comandos de voz y a comandos rápidos.

### 2.1. Activación por Voz: "Amais"

Para iniciar una conversación o darle una orden, use la palabra clave: **"Amais"**.

> **Ejemplo:**
> **Usted:** "Amais, limpia el suelo de la cocina."
> **Robot T4:** "Entendido. Planificando la ruta para limpiar el suelo de la cocina. ¿Desea confirmar?"

El robot siempre pedirá confirmación para asegurar que ha entendido la tarea correctamente.

### 2.2. Comandos Rápidos

Para acciones que no requieren confirmación o para finalizar la interacción, use los siguientes comandos:

| Comando Rápido | Propósito | Nota |
| :--- | :--- | :--- |
| **Finish** | Finaliza la sesión de comunicación por voz o telemática. | El robot vuelve al modo de espera. |
| **Stop** | Detiene inmediatamente cualquier acción o movimiento en curso. | **Comando de emergencia.** No requiere confirmación. |

## 3. Programación de Tareas (Tareas Reiterables)

Puede programar tareas para que el robot las realice automáticamente a través de la aplicación móvil o de escritorio.

### 3.1. Tipos de Programación

1.  **Ilimitada (Semanal):** La tarea se repite cada semana en el día y hora definidos.
    > **Ejemplo:** Programar al robot para limpiar el baño todos los **Lunes a las 10:00 AM**.
2.  **Una Vez:** La tarea se realiza solo en la próxima ocurrencia del día y hora definidos.

### 3.2. Extensión de Tareas (Aprendizaje)

El robot aprende continuamente. Si realiza una tarea de forma satisfactoria, la aplicación le permitirá:

*   **Confirmar la Tarea:** Aceptar la secuencia de acciones como una nueva habilidad.
*   **Programar Tarea Nueva:** Añadir esa nueva habilidad al sistema de programación para uso futuro (ej. "Limpiar el baño del vecino").

## 4. Configuración de Comunicación LoRaWAN (868 MHz)

El robot T4 utiliza LoRaWAN para comunicarse con su dispositivo anfitrión (móvil/PC) sin necesidad de una red Wi-Fi o Internet.

### 4.1. Configuración de Frecuencia Regional

La frecuencia de 868 MHz es estándar en muchas regiones, pero debe asegurarse de que es legal en su zona.

1.  **Verifique su Región:** Consulte el mapa de frecuencias de LoRaWAN [2] o el sitio web de LoRa Antenna [1] para confirmar la frecuencia legal en su ubicación.
2.  **Ajuste en la Aplicación:** En la configuración de la aplicación T4, navegue a `Configuración de Red > LoRaWAN` y seleccione la frecuencia correcta (ej. 915 MHz para EE. UU.).

### 4.2. Conexión al Dispositivo Anfitrión

1.  **Descarga del Sistema:** Utilice su móvil o PC con conexión a Internet para descargar el software del robot T4.
2.  **Conexión Inicial:** El robot T4 actúa como un sensor de conexión. Coloque el dispositivo anfitrión cerca del robot.
3.  **Transferencia de Sistema:** El dispositivo anfitrión transferirá el sistema operativo personalizado (Kernel Linux) y el software de control al robot a través de la conexión LoRaWAN de corto alcance.

## 5. Modos de Operación Autónoma

El robot gestiona automáticamente su conexión y energía.

*   **Modo Local (Offline):** El robot utiliza su LLM cuantizado en el chip (TinyML) para la autonomía total.
*   **Modo Respaldo en la Nube (Online):** Cuando está conectado a Internet (a través de su dispositivo anfitrión o Wi-Fi), el robot utiliza el LLM Kimi K2 completo en la nube (CorticalLabs NPU) para un razonamiento más profundo y para sincronizar sus conocimientos.

---
## Referencias

[1] LoRa Antenna: Herramienta para averiguar la frecuencia LoRaWAN por zona.
[2] The Things Network: Mapa de la red LoRaWAN global.
[3] Aloha Mini: Plataforma robótica de código abierto utilizada como base.
