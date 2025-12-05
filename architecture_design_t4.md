# Diseño de Arquitectura del Proyecto T4: Robot de Producción Híbrido y Edge AI

## 1. Introducción y Requisitos Clave

El Proyecto T4 es la evolución del concepto Amalia Gamma, enfocado en la **producción, la autonomía total en el borde (Edge AI)** y la **interacción humano-robot (HRI)** sofisticada. El objetivo es crear una plataforma robótica que pueda funcionar con un **cerebro integrado** en hardware de bajo costo y alto rendimiento.

**Requisitos Clave del T4:**

1.  **Hardware Objetivo:** RPi 500+, Arduino UNO Q, PocketBeagle 2.
2.  **Cerebro Integrado:** Arquitectura MindOn-like para el control autónomo.
3.  **Kernel Personalizado:** Linux optimizado para robótica y Edge AI.
4.  **Comunicación:** LoRaWAN (868 MHz) para control *offline* y IoT.
5.  **Edge AI:** TinyML y LLM cuantizados en chip.
6.  **HRI Sofisticado:** Comando de voz "Amais" y comandos rápidos programables.
7.  **Arquitectura Híbrida:** Nube (Respaldo/Entrenamiento) y Borde (Autonomía).

## 2. Diseño del Cerebro Integrado (MindOn-like)

El "cerebro integrado" T4 se basa en la arquitectura **MindOn** [1], que divide el control robótico en tres capas principales: **Decisiones, Acciones y Movimiento**.

| Capa | Componente Principal | Tecnología | Rol en T4 |
| :--- | :--- | :--- | :--- |
| **Decisiones (LLM)** | **Kimi K2 Cuantizado** (Edge) / **Kimi K2** (Nube) | LLM/TinyML | Razonamiento, planificación de tareas, comprensión del lenguaje natural (HRI). |
| **Acciones (RL/IL)** | **Agente de Refuerzo** (SIMA 2/Genie 3) | Aprendizaje por Refuerzo/Imitación | Generación de políticas de acción a partir de la decisión del LLM. |
| **Movimiento (HAL)** | **Kernel Personalizado** + **HAL** | Linux RT/C++ | Traducción de políticas de acción a comandos de bajo nivel para actuadores. |

## 3. Kernel Linux Personalizado para Robótica

Para las placas RPi 500+ y PocketBeagle 2, se requiere un **Kernel Linux personalizado** para garantizar la baja latencia y el determinismo, cruciales para el control robótico.

### 3.1. Personalización del Kernel

1.  **Parche RT (Real-Time):** Aplicación del parche PREEMPT\_RT para convertir el kernel estándar en un kernel de tiempo real. Esto es vital para la capa de **Movimiento** (HAL).
2.  **Optimización de Módulos:** Deshabilitar módulos innecesarios (ej. gráficos avanzados si no se usan) para reducir la huella de memoria y el consumo de energía.
3.  **Integración de Drivers:** Inclusión directa de *drivers* para los módulos LoRaWAN (868 MHz) y los controladores de motor específicos del robot.

### 3.2. Plataformas de Hardware y Rol

| Plataforma | Arquitectura | Sistema Operativo Base | Rol Principal en T4 |
| :--- | :--- | :--- | :--- |
| **RPi 500+** | ARM64 | Linux (Kernel RT Personalizado) | **Cerebro Principal:** Ejecución de LLM Cuantizado, Agente RL, HRI. |
| **PocketBeagle 2** | ARM Cortex-A53 | Linux (Kernel RT Personalizado) | **Cerebro Secundario/Control:** Fusión de sensores, control de movimiento de baja latencia. |
| **Arduino UNO Q** | Microcontrolador/Linux | Linux (Debian) + Microcontrolador | **Gateway/Control de Bajo Nivel:** Interfaz directa con actuadores, gestión de LoRaWAN. |

## 4. Comunicación LoRaWAN (868 MHz)

La comunicación LoRaWAN es esencial para el control *offline* y la conexión con un dispositivo anfitrión (móvil/PC) sin necesidad de Internet.

### 4.1. Arquitectura de Comunicación

1.  **Dispositivo Anfitrión (Móvil/PC):** Ejecuta una aplicación cliente que contiene el **programa de órdenes** y la interfaz de voz.
2.  **Gateway LoRa (Arduino UNO Q/Módulo):** Actúa como un *sensor* de conexión, recibiendo los comandos del anfitrión a través de LoRaWAN (868 MHz) y reenviándolos al Cerebro Principal (RPi 500+) a través de una interfaz local (ej. UART/SPI).
3.  **Protocolo:** Se utilizará un protocolo de mensajes ligero sobre LoRaWAN para enviar comandos de voz tokenizados y comandos rápidos (ej. "Amais", "Finish", "Stop").

### 4.2. Personalización de Frecuencias

El software debe permitir la selección de frecuencias por región para cumplir con las regulaciones locales, utilizando la banda de 868 MHz (Europa) como base, pero con la capacidad de cambiar a 915 MHz (EE. UU.) o 433 MHz (Asia) según la configuración del usuario.

*   **Implementación:** Se incluirá un archivo de configuración (`lorawan_config.json`) y una función en el **Manual de Usuario** para consultar mapas de red (ej. The Things Network [2]) y ajustar la frecuencia.

## 5. Edge AI: TinyML y LLM en Chip

La ejecución de modelos de IA en el borde se logra mediante la combinación de TinyML y LLM cuantizados.

*   **TinyML:** Se utilizará para tareas de percepción de baja latencia (ej. detección de la palabra clave "Amais", clasificación de objetos) en microcontroladores (Arduino UNO Q).
*   **LLM Cuantizado:** El modelo Kimi K2 se cuantizará (ej. GGUF Q4) para ejecutarse en el RPi 500+ para el razonamiento y la respuesta conversacional.

## 6. Interacción Humano-Robot (HRI)

### 6.1. Comando de Voz "Amais"

El comando de voz de activación se cambia a **"Amais"** para diferenciarlo de otros asistentes.

*   **Flujo de Comunicación:**
    1.  El robot escucha constantemente la palabra clave **"Amais"** (TinyML en el borde).
    2.  Al detectar "Amais", el robot activa el micrófono completo y envía la grabación de voz al LLM (local o en la nube).
    3.  El robot responde con su voz (utilizando la ruta de LLMs Amalia) y espera la siguiente orden.

### 6.2. Comandos Rápidos Programables

Se implementará un sistema de comandos rápidos programables (ej. "Finish", "Stop") que se pueden definir como tareas únicas o reiterables (semanales).

*   **Almacenamiento:** Los comandos se almacenarán en una base de datos local (ej. SQLite) y se sincronizarán con la nube.
*   **Programación:** La interfaz de usuario (móvil/PC) permitirá programar tareas reiterables (ej. "limpiar el baño todos los Lunes").
*   **Extensión de Tareas:** El sistema permitirá al usuario añadir nuevas tareas bien realizadas al *dataset* de entrenamiento (feedback, votaciones, RL), extendiendo las capacidades del robot.

---
## Referencias

[1] MindOn Robotics: Arquitectura de cerebro robótico avanzado.
[2] The Things Network: Mapa de frecuencias LoRaWAN por región.
[3] Raspberry Pi 500: Especificaciones técnicas y capacidades de Edge AI.
[4] Arduino UNO Q: Características de la placa con Linux integrado.
[5] PocketBeagle 2: Uso de Sitara AM6254 para sistemas embebidos.
