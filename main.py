import tkinter as tk
from src.view.ProcessSimulatorApp import ProcessSimulatorApp

if __name__ == "__main__":
    # Crear la ventana principal de la interfaz gráfica
    root = tk.Tk()

    # Instanciar la clase ProcessSimulatorApp (que está en el paquete view)
    app = ProcessSimulatorApp(root)

    # Iniciar el loop de la interfaz gráfica
    root.mainloop()
