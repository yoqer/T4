"""
t4_main_controller.py - Controlador Principal del Robot T4 (Ejecutado en RPi 500+ o PocketBeagle 2)

Implementa la lógica del cerebro MindOn-like, TinyML para la palabra clave y la interfaz LoRaWAN.
"""

import json
import time
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Simulación de Módulos ---

class TinyMLEngine:
    """Simula la detección de la palabra clave 'Amais' usando TinyML."""
    def __init__(self):
        logging.info("TinyML Engine inicializado para detección de palabra clave.")
        self.keyword = "amais"

    def listen_for_keyword(self, audio_input: str) -> bool:
        """Devuelve True si se detecta la palabra clave."""
        return self.keyword in audio_input.lower()

class LoRaWANInterface:
    """Simula la comunicación LoRaWAN a 868 MHz."""
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        self.frequency = self.config['frequency_mhz']
        logging.info(f"LoRaWAN Interface inicializada en {self.config['region']} ({self.frequency} MHz).")

    def send_command(self, command: str) -> bool:
        """Envía un comando al dispositivo anfitrión (móvil/PC)."""
        logging.info(f"LoRaWAN: Enviando comando '{command}' al anfitrión.")
        # Simulación de transmisión a 868 MHz
        return True

    def receive_data(self) -> str:
        """Simula la recepción de datos (órdenes, actualizaciones) desde el anfitrión."""
        # En un entorno real, esto sería un bucle de escucha.
        if time.time() % 10 < 2: # Simulación de recepción ocasional
            return "ORDEN: limpiar el suelo de la cocina"
        return ""

class MindOnBrain:
    """Arquitectura MindOn-like: Decisiones, Acciones, Movimiento."""
    def __init__(self, hal_interface):
        self.hal = hal_interface
        self.tiny_ml = TinyMLEngine()
        self.llm_local = LLMLocalEngine()
        self.task_scheduler = TaskScheduler()
        logging.info("MindOn Brain (Cerebro Integrado) listo.")

    def process_audio_input(self, audio_input: str):
        """Procesa la entrada de audio para comandos HRI."""
        if self.tiny_ml.listen_for_keyword(audio_input):
            logging.info("Palabra clave 'Amais' detectada. Activando LLM.")
            
            # 1. Decisión (LLM Local/Nube)
            response = self.llm_local.process_command(audio_input)
            
            # 2. Acción (Planificación)
            if "limpiar" in response:
                self.task_scheduler.schedule_task("Limpieza", "Limpiar el área especificada")
                self.hal.set_actuator_command("voice_module", {"speak": response})
            elif "finish" in response.lower():
                logging.info("Comando rápido 'Finish' detectado. Finalizando sesión de comunicación.")
                self.hal.set_actuator_command("voice_module", {"speak": "Sesión finalizada. En modo de espera."})
            elif "stop" in response.lower():
                logging.warning("Comando rápido 'Stop' detectado. Deteniendo todas las acciones.")
                self.hal.set_actuator_command("actuators", {"stop_all": True})
            else:
                self.hal.set_actuator_command("voice_module", {"speak": response})

    def run_autonomous_cycle(self):
        """Bucle principal de operación autónoma."""
        logging.info("Iniciando ciclo autónomo...")
        
        # 1. Comprobar órdenes LoRaWAN
        lora_data = self.lora.receive_data()
        if lora_data:
            logging.info(f"Nueva orden recibida vía LoRaWAN: {lora_data}")
            self.process_audio_input(lora_data) # Reutilizar el procesamiento de comandos

        # 2. Ejecutar tareas programadas
        self.task_scheduler.execute_next_task(self.hal)

class LLMLocalEngine:
    """Simula el LLM cuantizado en el chip (RPi 500+)."""
    def __init__(self):
        logging.info("LLM Local (Cuantizado) cargado y listo.")

    def process_command(self, command: str) -> str:
        """Simula el razonamiento del LLM."""
        if "limpiar el suelo" in command:
            return "Entendido. Planificando la ruta para limpiar el suelo de la cocina."
        elif "amais" in command.lower():
            return "Hola, soy T4. ¿Cuál es tu orden?"
        return "No estoy seguro de haber entendido. ¿Podrías repetir la orden?"

class TaskScheduler:
    """Gestión de comandos rápidos y tareas programadas."""
    def __init__(self):
        self.tasks = []
        logging.info("Task Scheduler inicializado.")

    def schedule_task(self, name: str, description: str, repeat: str = "once"):
        """Programa una nueva tarea."""
        self.tasks.append({"name": name, "desc": description, "repeat": repeat, "status": "pending"})
        logging.info(f"Tarea programada: {name} ({repeat}).")

    def execute_next_task(self, hal):
        """Ejecuta la siguiente tarea pendiente."""
        if self.tasks:
            task = self.tasks.pop(0)
            logging.info(f"Ejecutando tarea: {task['name']}")
            # Simulación de ejecución a través de HAL
            hal.set_actuator_command("mobility", {"move": "forward"})
            hal.set_actuator_command("mobility", {"move": "stop"})
            logging.info(f"Tarea {task['name']} completada.")
            
            if task['repeat'] == 'weekly':
                self.schedule_task(task['name'], task['desc'], task['repeat']) # Reprogramar

class HALInterface:
    """HAL simplificado para el T4."""
    def __init__(self):
        logging.info("HAL T4 inicializado.")

    def set_actuator_command(self, actuator_id: str, command: Dict[str, Any]):
        """Envía un comando al actuador."""
        logging.debug(f"HAL: Comando para {actuator_id}: {command}")
        # En un entorno real, esto se comunicaría con el microcontrolador (Arduino UNO Q)

# --- Bucle Principal ---

if __name__ == "__main__":
    # Inicializar componentes
    hal = HALInterface()
    brain = MindOnBrain(hal)
    brain.lora = LoRaWANInterface(config_path="lorawan_config.json") # Conectar LoRaWAN

    # Simulación de comandos rápidos programables
    brain.task_scheduler.schedule_task("Limpieza Semanal", "Limpiar el baño", "weekly")

    # Bucle de operación
    while True:
        try:
            brain.run_autonomous_cycle()
            time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Controlador T4 detenido.")
            break
