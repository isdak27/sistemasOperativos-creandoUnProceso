import time

class Process:
    def __init__(self, pid, duration, io_duration=0):
        self.pid = pid
        self.duration = duration  # Duración total del proceso en segundos
        self.io_duration = io_duration  # Duración simulada de operación de E/S en segundos
        self.state = "ready"  # Estados posibles: ready, running, waiting, terminated

    def run(self):
        self.state = "running"
        print(f"Process {self.pid} is running. (Duration: {self.duration}s)")
        time.sleep(self.duration)  # Simulamos el tiempo de procesamiento del CPU

        if self.io_duration > 0:
            self.state = "waiting"
            print(f"Process {self.pid} is performing I/O. (Duration: {self.io_duration}s)")
            time.sleep(self.io_duration)  # Simulamos la espera de E/S

        self.state = "terminated"
        print(f"Process {self.pid} has terminated.")
