# Guía de Despliegue del Proyecto T4: Robot con TinyML y Zephyr

## 1. Resumen Ejecutivo

El **Proyecto T4** es una plataforma robótica de producción lista para desplegar, que combina:

*   **Kernel Linux RT Personalizado** para el Cerebro Principal (RPi 500+, PocketBeagle 2).
*   **Zephyr RTOS** para Gateways de Sensores Inteligentes (ESP32, Arduino UNO Q).
*   **TinyML** para la inferencia en el borde con baja latencia y consumo mínimo de energía.
*   **LoRaWAN (868 MHz)** para la comunicación *offline* entre sensores y el cerebro principal.
*   **HRI Sofisticado** con el comando de voz **"Amais"** para la interacción natural.

## 2. Estructura del Proyecto

```
T4_Project/
├── README.md                                  # Visión general del proyecto
├── architecture_design_t4.md                  # Diseño de arquitectura detallado
├── developer_manual.md                        # Manual para desarrolladores
├── user_manual.md                             # Manual de usuario
├── rtos_integration_and_tinyml_training.md    # Guía de integración RTOS y TinyML
├── t4_main_controller.py                      # Controlador principal (simulación)
├── lorawan_config.json                        # Configuración de LoRaWAN
├── requirements.txt                           # Dependencias de Python
├── LICENSE                                    # Licencia Apache 2.0
├── tinyml_zephyr_slides.md                    # Contenido de la presentación
└── tinyml_zephyr_presentation/                # Presentación HTML
    ├── title_slide.html
    ├── architecture_overview.html
    ├── data_collection.html
    ├── model_training.html
    ├── deployment.html
    └── communication.html
```

## 3. Instrucciones de Despliegue

### 3.1. Instalación del Kernel Linux RT (RPi 500+ / PocketBeagle 2)

1.  **Descarga del Código Fuente:**
    ```bash
    git clone --depth=1 https://github.com/raspberrypi/linux.git -b rpi-6.6.y /usr/src/linux-rpi
    ```

2.  **Aplicación del Parche RT:**
    ```bash
    wget https://www.kernel.org/pub/linux/kernel/projects/rt/6.6/patch-6.6-rt1.patch.xz
    xzcat patch-6.6-rt1.patch.xz | patch -p1
    ```

3.  **Compilación:**
    ```bash
    make menuconfig  # Habilitar PREEMPT_RT
    make -j$(nproc)
    make modules_install
    make install
    ```

### 3.2. Despliegue de Zephyr en ESP32

1.  **Instalación de Zephyr SDK:**
    ```bash
    git clone https://github.com/zephyrproject-rtos/zephyr.git
    cd zephyr
    pip3 install -r scripts/requirements.txt
    ```

2.  **Creación del Proyecto Zephyr para ESP32:**
    ```bash
    west init -m https://github.com/zephyrproject-rtos/zephyr.git esp32_project
    cd esp32_project
    west update
    ```

3.  **Compilación y Flasheo:**
    ```bash
    west build -b esp32_devkitc samples/hello_world
    west flash
    ```

### 3.3. Entrenamiento de TinyML en Edge Impulse

1.  **Crear Proyecto en Edge Impulse Studio:**
    *   Inicie sesión en [https://studio.edgeimpulse.com](https://studio.edgeimpulse.com)
    *   Cree un nuevo proyecto de "Time Series Data"

2.  **Recolección de Datos:**
    *   Conecte el ESP32 con `edge-impulse-daemon`
    *   Recoja datos de temperatura en tres estados: Normal, Alta, Baja

3.  **Entrenamiento del Modelo:**
    *   Defina el Impulso (Bloque de Procesamiento + Bloque de Aprendizaje)
    *   Entrene el modelo hasta alcanzar >95% de precisión

4.  **Generación de Código C++:**
    *   Vaya a "Deployment" y seleccione "C++ Library"
    *   Descargue la librería y copie en el proyecto Zephyr

### 3.4. Configuración de LoRaWAN

1.  **Edite `lorawan_config.json`:**
    ```json
    {
        "region": "EU868",
        "frequency_mhz": 868.0,
        "lora_device_id": "T4_ROBOT_001",
        "lora_app_key": "YOUR_LORAWAN_APP_KEY",
        "lora_dev_eui": "YOUR_LORAWAN_DEV_EUI"
    }
    ```

2.  **Registre el dispositivo en The Things Network:**
    *   Visite [https://www.thethingsnetwork.org](https://www.thethingsnetwork.org)
    *   Registre su ESP32 como un dispositivo LoRaWAN

## 4. Uso del Robot T4

### 4.1. Activación por Voz

```
Usuario: "Amais, limpia el suelo de la cocina."
Robot T4: "Entendido. Planificando la ruta para limpiar el suelo de la cocina. ¿Desea confirmar?"
```

### 4.2. Comandos Rápidos

*   **"Finish":** Finaliza la sesión de comunicación.
*   **"Stop":** Detiene inmediatamente cualquier acción en curso.

### 4.3. Programación de Tareas

Utilice la aplicación móvil o de escritorio para programar tareas reiterables (ej. "Limpiar el baño todos los Lunes a las 10:00 AM").

## 5. Presentación de Diapositivas

La presentación sobre el despliegue de TinyML en ESP32 con Zephyr se encuentra en:

```
tinyml_zephyr_presentation/
├── title_slide.html
├── architecture_overview.html
├── data_collection.html
├── model_training.html
├── deployment.html
└── communication.html
```

Abra `title_slide.html` en un navegador web para ver la presentación completa.

## 6. Soporte y Documentación

*   **Manual del Desarrollador:** `developer_manual.md`
*   **Manual de Usuario:** `user_manual.md`
*   **Diseño de Arquitectura:** `architecture_design_t4.md`
*   **Integración RTOS y TinyML:** `rtos_integration_and_tinyml_training.md`

## 7. Licencia

Este proyecto se distribuye bajo la **Apache License 2.0**.

---

**Proyecto T4: Robótica de Producción con Edge AI**
*Desarrollado por Manus AI*
*Repositorio: https://github.com/yoqer/T4*
