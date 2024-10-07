import threading
from src.logic.Process import Process

class RoundRobinScheduler:
    def __init__(self, quantum, callback=None):
        self.quantum = quantum  # Quantum de tiempo en segundos
        self.process_queue = []  # Cola de procesos
        self.condition = threading.Condition()  # Condición para coordinar la ejecución de procesos
        self.callback = callback  # Callback para actualizar la interfaz

    def add_process(self, process):
        """Añade un proceso a la cola."""
        self.process_queue.append(process)
        if self.callback:
            self.callback(process.pid, "ready")  # Notificar a la interfaz que el proceso está "ready"
        print(f"Added Process {process.pid} to the queue.")

    def run_process_for_quantum(self, process):
        """Simula la ejecución de un proceso durante el quantum de tiempo."""
        if process.state == "terminated":
            return

        # Simular ejecución por el quantum o menos si el proceso es más corto
        remaining_duration = process.duration
        if remaining_duration <= self.quantum:
            process.run()  # Se ejecuta hasta que termine
        else:
            print(f"Process {process.pid} is running for {self.quantum}s. (Remaining: {process.duration}s)")
            process.duration -= self.quantum

            if self.callback:
                self.callback(process.pid, "running")  # Notificar a la interfaz que el proceso está "running"

            with self.condition:
                self.condition.wait_for(lambda: False, timeout=self.quantum)  # Esperar quantum de tiempo
                print(f"Process {process.pid} has paused. (Remaining: {process.duration}s)")
                process.state = "waiting"

            if self.callback:
                self.callback(process.pid, "waiting")  # Notificar a la interfaz que el proceso está "waiting"

    def schedule(self):
        """Planifica y ejecuta los procesos utilizando el algoritmo Round Robin."""
        print("Starting Round Robin Scheduling...")
        while self.process_queue:
            process = self.process_queue.pop(0)

            if process.state != "terminated":
                self.run_process_for_quantum(process)  # Ejecutar el proceso por el quantum de tiempo

                if process.state != "terminated":
                    # Si el proceso no ha terminado, lo volvemos a poner en la cola
                    self.process_queue.append(process)

            # En lugar de usar sleep, esperamos activamente con la condición para controlar el quantum
            with self.condition:
                self.condition.wait_for(lambda: False, timeout=0.1)  # Espera entre cambios de proceso

        print("All processes have been executed.")