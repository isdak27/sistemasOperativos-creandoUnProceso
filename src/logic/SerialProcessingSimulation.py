from src.logic.Process import Process

class SerialProcessingSimulation:
    def __init__(self, processes=None):
        """Inicializa la simulación de procesamiento en serie con una cola de procesos."""
        # Si no se proporcionan procesos, inicializamos una lista vacía
        self.process_queue = processes if processes is not None else []
        self.current_process = None

    def add_process(self, process):
        """Añade un proceso a la cola."""
        self.process_queue.append(process)
        print(f"Added Process {process.pid} to the queue.")

    def start_simulation(self):
        """Inicia la simulación de procesamiento en serie."""
        print("Starting Serial Processing Simulation...")
        while self.process_queue:
            # Tomamos el primer proceso de la cola
            self.current_process = self.process_queue.pop(0)
            print(f"Scheduling Process {self.current_process.pid}...")
            self.current_process.run()  # Ejecutamos el proceso secuencialmente
        print("All processes have been executed.")
