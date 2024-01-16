import threading
import time


class Demonio(threading.Thread):
    def _init_(self):
        super()._init_()
        self.activo = False

    def run(self):
        print("Demonio iniciado.")
        self.activo = True
        while self.activo:
            print("El demonio está corriendo...\n")
            time.sleep(5)  # Intervalo entre mensajes
        print("Demonio detenido.")

    def detener(self):
        self.activo = False