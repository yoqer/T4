# Despliegue de TinyML en el Borde: ESP32 con Zephyr RTOS

## 1. TinyML en el Proyecto T4: Gateways de Sensores Inteligentes

El Proyecto T4 utiliza **TinyML** para dotar de inteligencia a los sensores de bajo consumo, transformándolos en **Gateways de Sensores Inteligentes** que se comunican con el Cerebro Principal (Linux RT) a través de LoRaWAN.

*   **Objetivo:** Clasificación de datos en el chip para reducir la latencia y el consumo de energía.
*   **Hardware:** Microcontroladores de baja potencia (ej. ESP32, Arduino UNO Q).
*   **Comunicación:** LoRaWAN (868 MHz) para enviar solo el resultado de la inferencia (ej. "Temperatura: Alta").

## 2. Arquitectura de Software: La Elección de Zephyr RTOS

**Zephyr** [1] es un RTOS de código abierto ideal para la gestión determinista y de baja huella de los sensores y la pila LoRaWAN.

*   **Determinismo:** Garantiza la ejecución de tareas críticas en tiempo real, esencial para el control robótico de bajo nivel.
*   **Baja Huella:** Su diseño modular permite incluir solo los componentes necesarios, optimizando el uso de memoria y energía.
*   **Soporte TFLite Micro:** Proporciona un entorno robusto para la ejecución de modelos de **TensorFlow Lite Micro** [2].

## 3. Fase 1: Recolección y Etiquetado de Datos (Edge Impulse)

La plataforma **Edge Impulse** [3] simplifica el ciclo de vida de TinyML, desde la recolección hasta el despliegue.

*   **Conexión del Sensor:** El ESP32 se conecta a Edge Impulse Studio a través de la CLI (`edge-impulse-daemon`).
*   **Recolección de Datos:** Se capturan series temporales del sensor de temperatura en diferentes condiciones (ej. "Normal", "Alta", "Baja").
*   **Etiquetado:** Los datos se etiquetan con precisión para crear el *dataset* de entrenamiento.

## 4. Fase 2: Diseño del Impulso y Entrenamiento del Modelo

El "Impulso" define la tubería de procesamiento y aprendizaje automático.

*   **Bloque de Procesamiento:** Se utiliza el bloque de **Series Temporales** para extraer características clave (ej. media, desviación estándar) de la señal de temperatura.
*   **Bloque de Aprendizaje:** Se selecciona un modelo de **Clasificación (Keras/Árbol de Decisión)**.
*   **Optimización:** El entrenamiento se centra en maximizar la precisión mientras se minimiza la huella de memoria y el tiempo de inferencia.

## 5. Fase 3: Despliegue en el Borde (TFLite Micro y Zephyr)

El modelo entrenado se convierte en código C++ optimizado para el microcontrolador.

*   **Generación de Código:** Edge Impulse genera una **Librería C++** que contiene el modelo TFLite Micro.
*   **Integración en Zephyr:** El código C++ se integra en el proyecto Zephyr del ESP32.
*   **Inferencia en el Chip:** El *firmware* de Zephyr ejecuta el modelo TFLite Micro para clasificar la temperatura en tiempo real.

## 6. Fase 4: Comunicación Inteligente con LoRaWAN

El resultado de la inferencia se utiliza para la comunicación eficiente con el Cerebro Principal del T4.

*   **Mensaje Inteligente:** En lugar de enviar datos brutos de temperatura, el ESP32 (con Zephyr) envía solo el resultado de la clasificación (ej. "Temp: Alta").
*   **Eficiencia:** Esto reduce drásticamente el tamaño del mensaje, optimizando el uso de la banda LoRaWAN y el consumo de energía.
*   **HAL Bridge:** El Cerebro Principal (Linux RT) recibe el mensaje clasificado y lo utiliza para la toma de decisiones de alto nivel.

---
## Referencias

[1] Zephyr Project: RTOS de código abierto para IoT.
[2] TensorFlow Lite Micro: Librería de inferencia para microcontroladores.
[3] Edge Impulse: Plataforma para el desarrollo de TinyML.
