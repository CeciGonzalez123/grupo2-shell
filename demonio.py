import threading
import time


class Demonio(threading.Thread):
    def __init__(self):
        super().__init__()
        self.activo = False

    def run(self):
        print("Demonio iniciado.")
        self.activo = True
        while self.activo:  # Mantener el demonio activo hasta que se detenga
            print(f" ... ", end="")
            time.sleep(1)  # Simula trabajo;
        # Este mensaje se mostrará cuando el demonio se detenga
        print("Demonio detenido...")

    def detener(self):
        if not self.activo:
            print("Demonio no ha sido iniciado.")
        else:
            self.activo = False
