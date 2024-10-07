import threading


class BatchProcessingSimulation:
    def __init__(self, mode="mono"):
        """Constructor que inicializa el modo de simulación y otros atributos."""
        self.mode = mode  # Almacenar el modo de simulación
        self.process_queue = []  # Cola de procesos a simular
        self.current_processes = []  # Lista de procesos actuales
        self.semaphore = threading.Semaphore(2)  # Semáforo para limitar procesos concurrentes

    def add_process(self, process):
        """Agrega un proceso a la cola de la simulación."""
        self.process_queue.append(process)

    def start_mono_simulation_with_callback(self, callback):
        """Simula procesamiento por lotes en mono-programación con callback."""
        print("Starting Batch Processing Simulation in Mono-programming mode...")
        while self.process_queue:
            process = self.process_queue.pop(0)
            callback(process.pid, "running")
            process.run()  # Ejecuta los procesos secuencialmente
            callback(process.pid, "terminated")
        print("All processes in the batch have been executed.")

    def start_multi_simulation_with_callback(self, callback):
        """Simula procesamiento por lotes en multi-programación con callback."""

        def process_runner(process):
            """Función que ejecuta un proceso individualmente."""
            self.semaphore.acquire()  # Adquirir recurso del semáforo
            try:
                callback(process.pid, "running")
                process.run()
                callback(process.pid, "terminated")
            finally:
                self.semaphore.release()  # Liberar recurso del semáforo
                self.current_processes.remove(process)

        print("Starting Batch Processing Simulation in Multi-programming mode...")
        while self.process_queue:
            process = self.process_queue.pop(0)
            self.current_processes.append(process)
            threading.Thread(target=process_runner, args=(process,)).start()

        # Esperar a que todos los procesos terminen
        while self.current_processes:
            with threading.Condition():
                pass

        print("All processes in the batch have been executed.")

    def start_simulation(self, callback):
        """Método genérico para comenzar la simulación según el modo seleccionado."""
        if self.mode == "mono":
            self.start_mono_simulation_with_callback(callback)
        elif self.mode == "multi":
            self.start_multi_simulation_with_callback(callback)