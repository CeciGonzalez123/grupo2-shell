import threading
import time


class Demonio(threading.Thread):
    def _init_(self):
        super()._init_()
        self.activo = False

    def run(self):
        print("Demonio iniciado.")
        self.activo = True
       

    def detener(self):
        self.activo = False
        print("Demonio detenido.")