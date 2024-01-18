import ftplib
import logger
import logging
import os


def transferir_ftp(hostname, username, password, archivo, destino=None):
    try:
        with ftplib.FTP(hostname, username, password) as ftp:
            with open(archivo, 'rb') as file:
                if destino is None:
                    destino = os.path.basename(archivo)
                ftp.storbinary(f'STOR {destino}', file)
        print(
            f"Transferencia a Host {hostname} de '{archivo}' ")
        registrar_transferencia(hostname, archivo)
    except Exception as e:
        print(f"Error al enviar via ftp: {e}")


def registrar_transferencia(hostname, archivo):
    logger.log(
        f"Transferencia a Host {hostname} de '{archivo}' ", "ftp", logging.INFO)
