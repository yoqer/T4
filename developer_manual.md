# Manual del Desarrollador del Proyecto T4: Plataforma de Hosting y Respaldo en la Nube

## 1. Introducción

Este manual proporciona una guía detallada para desarrolladores que trabajan en la infraestructura de *hosting* y la capa de respaldo en la nube del Proyecto T4. El objetivo es mantener la **continuidad operativa** y facilitar el **entrenamiento en multiversos** para el robot.

## 2. Arquitectura de Hosting Híbrida

El sistema T4 utiliza una arquitectura híbrida: el **Borde (Edge)** para la autonomía y la **Nube (Hosting)** para el respaldo, el razonamiento complejo y el entrenamiento.

| Componente | Ubicación | Tecnología Clave | Función de Respaldo/Entrenamiento |
| :--- | :--- | :--- | :--- |
| **T4 Robot (Edge)** | RPi 500+, Arduino UNO Q | TinyML, LoRaWAN, Kernel RT | Autonomía, control de bajo nivel, HRI local. |
| **API Gateway** | Hosting (Nube) | JWT, HTTPS | Punto de entrada seguro para la comunicación robot-nube. |
| **LLM Engine (Kimi K2)** | Hosting (Nube) | **CorticalLabs NPU** | Respaldo de razonamiento, actualización de *datasets* y conocimientos. |
| **Training Multiverse** | Hosting (Nube) | NVIDIA Omniverse / Google Genie 3 | Entorno para el entrenamiento del Agente RL/IL. |

## 3. Configuración de la Plataforma de Hosting

### 3.1. Requisitos del Servidor

Se recomienda un servidor con las siguientes especificaciones mínimas para el *hosting* del LLM y el entorno de entrenamiento:

*   **CPU:** 8 vCPUs (Intel/AMD)
*   **RAM:** 32 GB
*   **GPU:** NVIDIA A100 (para aceleración de entrenamiento y LLM Kimi K2)
*   **Sistema Operativo:** Ubuntu Server 22.04 LTS

### 3.2. Despliegue del LLM en la Nube (CorticalLabs NPU)

El LLM Kimi K2 se ejecuta en el NPU de CorticalLabs para un rendimiento óptimo.

1.  **Instalación del SDK:** Instale el SDK de CorticalLabs para Python.
    ```bash
    pip3 install cortical-labs-sdk
    ```
2.  **Configuración de la API:** Configure la clave de API en el archivo de entorno del servidor.
    ```bash
    export CORTICAL_API_KEY="YOUR_API_KEY"
    ```
3.  **Módulo de Respaldo:** El módulo `cloud_llm_backup.py` (a crear) se encargará de la comunicación.

```python
# cloud_llm_backup.py (Simulación de la interfaz)
from cortical_labs_sdk import KimiK2Client

def get_cloud_response(prompt: str) -> str:
    """Obtiene una respuesta del LLM Kimi K2 en el NPU."""
    client = KimiK2Client()
    response = client.generate(model="kimi-k2-full", prompt=prompt)
    return response.text
```

## 4. Conexión de IoT y Respaldo de Datos

### 4.1. Sincronización de Conocimiento (Chit Dataset)

El robot T4 mantiene un *dataset* de conocimiento local (Chit Dataset) que debe sincronizarse con la nube para el respaldo y la actualización de modelos.

*   **Protocolo:** Se utiliza un protocolo de sincronización basado en MQTT sobre el API Gateway.
*   **Flujo:** El robot (Edge) envía periódicamente fragmentos de datos de entrenamiento (nuevas tareas aprendidas, *feedback* de usuario) al *hosting*. El *hosting* los integra en el *dataset* maestro y entrena una nueva versión del modelo.

### 4.2. Entrenamiento en Multiversos (Omniverse/Genie 3)

El *hosting* es la plataforma central para el entrenamiento del Agente RL/IL.

1.  **Configuración de Entornos:**
    *   **NVIDIA Omniverse:** Requiere la instalación de Isaac Sim en el servidor con aceleración GPU.
    *   **Google Genie 3:** Requiere acceso a la API de Genie 3 para la generación de mundos programables.
2.  **Flujo de Entrenamiento:**
    *   El usuario o el **Suna AI Navigator Agent** (ejecutado en el *hosting*) define una tarea.
    *   El agente genera un escenario en el Multiverso (Omniverse o Genie 3).
    *   El robot virtual aprende la acción.
    *   La política de acción aprendida se envía al **Update Manager** del robot (Edge) a través del API Gateway.

## 5. Personalización del Kernel Linux (Guía Avanzada)

Para desarrolladores que necesiten optimizar el rendimiento de baja latencia en RPi 500+ o PocketBeagle 2.

1.  **Descarga del Código Fuente:**
    ```bash
    git clone --depth=1 https://github.com/raspberrypi/linux.git -b rpi-6.6.y /usr/src/linux-rpi
    # O el código fuente del kernel de PocketBeagle 2
    ```
2.  **Aplicación del Parche RT:**
    ```bash
    wget https://www.kernel.org/pub/linux/kernel/projects/rt/6.6/patch-6.6-rt1.patch.xz
    xzcat patch-6.6-rt1.patch.xz | patch -p1
    ```
3.  **Configuración y Compilación:**
    ```bash
    make menuconfig # Habilitar PREEMPT_RT y deshabilitar módulos innecesarios
    make -j$(nproc)
    make modules_install
    make install
    ```
    **Nota:** Este proceso es sensible a la arquitectura y debe realizarse en la plataforma de destino o mediante compilación cruzada.

## 6. Integración de la Comunicación LoRaWAN

La comunicación LoRaWAN (868 MHz) es el canal de control *offline*.

*   **Módulo de Control:** El módulo `lorawan_interface.py` (a crear) en el robot gestiona la conexión con el módulo físico (ej. ASR6501 en el Arduino UNO Q).
*   **Protocolo de Órdenes:** Los comandos de voz (ej. "Amais, limpia el suelo") se tokenizan en el dispositivo anfitrión y se envían como mensajes cortos a través de LoRaWAN. El robot (Edge) recibe el token y lo procesa con su LLM local.

---
*Este manual es para uso interno del equipo de desarrollo y detalla la implementación de la infraestructura de respaldo y entrenamiento.*
