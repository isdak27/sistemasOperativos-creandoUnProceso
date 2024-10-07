import tkinter as tk
from tkinter import ttk
import time
from src.logic.Process import Process
from src.logic.RoundRobinScheduler import RoundRobinScheduler
from src.logic.BatchProcessingSimulation import BatchProcessingSimulation
from src.logic.SerialProcessingSimulation import SerialProcessingSimulation


class ProcessSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Process Simulation")

        self.simulation_mode = tk.StringVar(value="mono")  # Modo de simulación por defecto: mono
        self.scheduler = None  # Planificador dependiendo del modo
        self.process_list = []  # Lista de procesos para simular
        self.quantum = 2  # Quantum por defecto para Round Robin
        self.start_time = 0  # Tiempo de inicio de la simulación
        self.elapsed_time_label = None  # Label para mostrar el tiempo transcurrido

        # Crear estilos personalizados
        self.create_styles()

        # Crear la interfaz gráfica
        self.create_widgets()

    def create_styles(self):
        """Crea estilos personalizados para los botones."""
        style = ttk.Style()
        style.configure('AddProcess.TButton', background='lightblue', padding=10)
        style.configure('StartSimulation.TButton', background='lightgreen', padding=10)

    def create_widgets(self):
        # Marco superior para la selección de simulación y entrada de procesos
        frame_top = ttk.Frame(self.root)
        frame_top.pack(pady=10)

        # Selector de modo de simulación
        ttk.Label(frame_top, text="Simulation Mode:").grid(row=0, column=0, padx=5)
        self.simulation_selector = ttk.Combobox(frame_top, textvariable=self.simulation_mode, state="readonly")
        self.simulation_selector['values'] = ('mono', 'multi', 'round-robin', 'serial')  # Agregando opción serial
        self.simulation_selector.grid(row=0, column=1, padx=5)
        self.simulation_selector.bind("<<ComboboxSelected>>", self.update_simulation_mode)

        # Marco para las entradas de proceso
        frame_process_input = ttk.Frame(self.root)
        frame_process_input.pack(pady=10)

        # Entradas para agregar procesos
        ttk.Label(frame_process_input, text="Process ID:").grid(row=0, column=0, padx=5)
        self.process_id_entry = ttk.Entry(frame_process_input)
        self.process_id_entry.grid(row=0, column=1, padx=5)

        ttk.Label(frame_process_input, text="Duration (s):").grid(row=0, column=2, padx=5)
        self.duration_entry = ttk.Entry(frame_process_input)
        self.duration_entry.grid(row=0, column=3, padx=5)

        ttk.Label(frame_process_input, text="I/O Duration (s):").grid(row=0, column=4, padx=5)
        self.io_duration_entry = ttk.Entry(frame_process_input)
        self.io_duration_entry.grid(row=0, column=5, padx=5)

        # Botón para agregar el proceso
        button_add_process = ttk.Button(frame_process_input, text="Add Process", command=self.add_process, style='AddProcess.TButton')
        button_add_process.grid(row=0, column=6, padx=5, sticky="ew")
        button_add_process.config(width=20)

        # Título para la lista de procesos
        ttk.Label(self.root, text="Processes In Queue:").pack(pady=5)

        # Lista de procesos
        self.process_listbox = tk.Listbox(self.root, height=10, width=50)
        self.process_listbox.pack(pady=10)

        # Panel para mostrar el estado de los procesos
        ttk.Label(self.root, text="Process States:").pack(pady=10)
        self.state_listbox = tk.Listbox(self.root, height=10, width=50)
        self.state_listbox.pack(pady=10)

        # Label para mostrar el tiempo transcurrido
        self.elapsed_time_label = ttk.Label(self.root, text="Elapsed Time: 0 seconds")
        self.elapsed_time_label.pack(pady=10)

        # Botón para iniciar la simulación
        start_simulation_button = ttk.Button(self.root, text="Start Simulation", command=self.start_simulation, style='StartSimulation.TButton')
        start_simulation_button.pack(pady=10)
        start_simulation_button.config(width=30)

    def update_simulation_mode(self, event):
        """Cambia el modo de simulación según la selección del usuario."""
        mode = self.simulation_mode.get()
        print(f"Selected simulation mode: {mode}")

    def add_process(self):
        """Añade un proceso a la lista de procesos y lo muestra en la interfaz."""
        try:
            pid = int(self.process_id_entry.get())
            duration = float(self.duration_entry.get())
            io_duration = float(self.io_duration_entry.get()) if self.io_duration_entry.get() else 0

            # Crear y añadir el proceso a la lista interna
            process = Process(pid, duration, io_duration)
            self.process_list.append(process)

            # Mostrar el proceso en la lista de la interfaz
            self.process_listbox.insert(tk.END, f"Process {pid}: Duration {duration}s, IO {io_duration}s")

            # Limpiar las entradas
            self.process_id_entry.delete(0, tk.END)
            self.duration_entry.delete(0, tk.END)
            self.io_duration_entry.delete(0, tk.END)

        except ValueError:
            print("Error: Por favor ingresa valores numéricos válidos para el ID, la duración y la duración de I/O.")

    def start_simulation(self):
        """Inicia la simulación basada en el modo seleccionado y registra el tiempo de inicio."""
        self.start_time = time.time()  # Registra el tiempo de inicio
        self.elapsed_time_label['text'] = "Elapsed Time: 0 seconds"  # Reinicia el tiempo transcurrido

        mode = self.simulation_mode.get()

        if mode == "mono":
            self.run_mono_simulation()
        elif mode == "multi":
            self.run_multi_simulation()
        elif mode == "round-robin":
            self.run_round_robin_simulation()
        elif mode == "serial":
            self.run_serial_simulation()

    def run_mono_simulation(self):
        """Inicia la simulación en modo mono-programación."""
        print("Starting Mono-programming Simulation...")
        simulation = BatchProcessingSimulation(mode="mono")

        # Agregar procesos a la simulación
        for process in self.process_list:
            simulation.add_process(process)

        # Iniciar simulación con el callback para actualizar la interfaz
        simulation.start_simulation(self.update_process_status)
        self.end_simulation()

    def run_multi_simulation(self):
        """Inicia la simulación en modo multi-programación."""
        print("Starting Multi-programming Simulation...")
        simulation = BatchProcessingSimulation(mode="multi")  # Pasamos el modo "multi"

        # Agregar procesos a la simulación
        for process in self.process_list:
            simulation.add_process(process)

        # Iniciar simulación con el callback para actualizar la interfaz
        simulation.start_simulation(self.update_process_status)
        self.end_simulation()  # Llama a la función que termina la simulación

    def run_round_robin_simulation(self):
        """Inicia la simulación en modo Round Robin."""
        print("Starting Round Robin Simulation...")
        self.scheduler = RoundRobinScheduler(self.quantum, callback=self.update_process_status)

        # Agregar procesos al planificador de Round Robin
        for process in self.process_list:
            self.scheduler.add_process(process)

        self.scheduler.schedule()
        self.end_simulation()

    def run_serial_simulation(self):
        """Inicia la simulación en modo de procesamiento en serie."""
        print("Starting Serial Simulation...")
        # Pasar la lista de procesos a la simulación
        simulation = SerialProcessingSimulation(processes=self.process_list)
        simulation.start_simulation()
        self.end_simulation()  # Llama a la función que termina la simulación

    def update_process_status(self, pid, status):
        """Actualiza el estado del proceso en la interfaz gráfica."""
        # Actualiza el panel de estados
        self.state_listbox.insert(tk.END, f"Process {pid}: {status}")

        # También actualiza la lista de procesos si es necesario
        for idx, process_text in enumerate(self.process_listbox.get(0, tk.END)):
            if process_text.startswith(f"Process {pid}"):
                # Actualizar el texto con el nuevo estado
                updated_text = f"{process_text} - {status}"
                self.process_listbox.delete(idx)
                self.process_listbox.insert(idx, updated_text)
                break

    def end_simulation(self):
        """Finaliza la simulación y calcula el tiempo total transcurrido."""
        elapsed_time = time.time() - self.start_time  # Calcula el tiempo transcurrido
        self.elapsed_time_label['text'] = f"Elapsed Time: {elapsed_time:.2f} seconds"  # Actualiza la etiqueta del tiempo