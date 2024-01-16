import ftplib
import logger
import logging


def transferir_ftp(hostname, username, password, archivo, destino):
    try:
        with ftplib.FTP(hostname, username, password) as ftp:
            with open(archivo, 'rb') as file:
                ftp.storbinary(f'STOR {destino}', file)
        registrar_transferencia(hostname, archivo, destino)

    except Exception as e:
        print(f"Error al enviar via ftp: {e}")


def registrar_transferencia(hostname, archivo, destino):
    logger.log(
        "Transferencia a Host {hostname} de '{archivo}' a '{destino}'\n", "ftp", logging.INFO)