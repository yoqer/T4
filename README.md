# Proyecto T4: Robot de Producción con Cerebro Integrado y Edge AI

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)
[![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-green.svg)](./developer_manual.md)
[![Powered by MindOn Architecture](https://img.shields.io/badge/Brain-MindOn--like-purple.svg)](./architecture_design_t4.md)

## 🚀 Visión General

El **Proyecto T4** es una plataforma robótica de código abierto diseñada para la **producción en masa** y la **autonomía total en el borde (Edge AI)**. Combina hardware de bajo costo y alto rendimiento (RPi 500+, Arduino UNO Q, PocketBeagle 2) con una arquitectura de software sofisticada, incluyendo un **Kernel Linux personalizado** y comunicación **LoRaWAN** para el control *offline*.

El robot T4 está diseñado para ser un **autómata** con un **Cerebro Integrado** (MindOn-like) que gestiona la toma de decisiones, las acciones y el movimiento.

---


![terminator-future-war](https://github.com/user-attachments/assets/7f896f40-7414-4881-8192-0265b8ce7112)




## 🧠 Arquitectura de Hardware y Cerebro Integrado

El T4 se basa en un diseño modular que permite el uso de varias placas con capacidad de "cerebro integrado".

### 1. Hardware Compatible

| Plataforma | Arquitectura | Rol Clave | Edge AI |
| :--- | :--- | :--- | :--- |
| **RPi 500+** | ARM64 | Cerebro Principal (LLM Local) | LLM Cuantizado (Kimi K2) |
| **Arduino UNO Q** | Linux/Microcontrolador | Gateway LoRaWAN, Control de Bajo Nivel | TinyML (Detección de "Amais") |
| **PocketBeagle 2** | ARM Cortex-A53 | Control de Movimiento RT, Fusión de Sensores | TinyML |

### 2. Arquitectura MindOn-like

El software sigue el modelo de cerebro robótico **MindOn**, dividiendo la inteligencia en capas:

*   **Decisiones:** Gestionadas por el LLM (Kimi K2) local o en la nube.
*   **Acciones:** Planificadas por un Agente de Refuerzo/Imitación (entrenado en Multiversos).
*   **Movimiento:** Ejecutado por el **Kernel Linux RT Personalizado** y la **HAL**.

## 🌐 Comunicación y HRI

### 1. LoRaWAN (868 MHz)

El T4 utiliza la banda de 868 MHz para la comunicación de largo alcance y el control *offline* con un dispositivo anfitrión (móvil/PC).

*   **Función:** Permite la descarga inicial del sistema y el envío de órdenes sin necesidad de Internet.
*   **Personalización:** La frecuencia es seleccionable por región a través de la aplicación de usuario.

### 2. Interacción Humano-Robot (HRI)

*   **Comando de Voz:** El robot responde a la palabra clave **"Amais"** (en lugar de "Amai") para iniciar la comunicación.
*   **Comandos Rápidos:** Incluye comandos de voz rápidos como **"Finish"** (finalizar sesión) y **"Stop"** (detener acción).
*   **Programación:** El software permite la programación de tareas reiterables (semanales) y la extensión de las capacidades del robot mediante el *feedback* del usuario.

## 🛠️ Desarrollo y Despliegue

### 1. Kernel Personalizado

El proyecto incluye la documentación para compilar un **Kernel Linux con parche RT** para garantizar la baja latencia en el control robótico.

### 2. Entrenamiento en Multiversos

El sistema está listo para conectarse a una plataforma de *hosting* (respaldo en la nube) que gestiona el entrenamiento en **Multiversos** (NVIDIA Omniverse o Google Genie 3) y actualiza los modelos del robot en tiempo real a través de la comunicación de banda 868 MHz.

---

## 📚 Documentación y Manuales

*   **Manual del Desarrollador:** [developer_manual.md](./developer_manual.md)
    *   Detalles de la implementación del *hosting*, la conexión al LLM en la nube y la personalización del Kernel.
*   **Manual de Usuario:** [user_manual.md](./user_manual.md)
    *   Guía de operación, programación de tareas y configuración de la comunicación LoRaWAN.
*   **Diseño de Arquitectura:** [architecture_design_t4.md](./architecture_design_t4.md)
    *   Detalles del Cerebro Integrado, TinyML y la arquitectura híbrida.

---
## 📜 Licencia

Este proyecto se distribuye bajo: **Apache License 2.0**.
Sin garantías, ni nuestra responsabilidad, solo para proyectos domesticos, sin necesidad de Seguridad.       
(No se recomienda en procesos de Identificacion sin Implementar Protocolos de Encriptacion y Seguridad.) 
---
## Referencias

[1] LoRa Antenna: Herramienta para averiguar la frecuencia LoRaWAN por zona.
[2] The Things Network: Mapa de la red LoRaWAN global.
[3] MindOn Robotics: Arquitectura de cerebro robótico avanzado.
[4] Raspberry Pi 500: Especificaciones y capacidades de Edge AI.
[5] Arduino UNO Q: Características de la placa con Linux integrado.
