import ftplib
import logger
import logging
import os


def transferir_ftp(archivo, destino=None):
    hostname = "ftp.dlptest.com"
    username = "dlpuser"
    password = "rNrKYTX9g7z3RgJRmxWuGHbeu"

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


def descargar_ftp(archivo, destino=None):
    hostname = "ftp.dlptest.com"
    username = "dlpuser"
    password = "rNrKYTX9g7z3RgJRmxWuGHbeu"

    try:
        # Conectar al servidor FTP
        with ftplib.FTP(hostname, username, password) as ftp:
            # Cambiar al directorio donde se encuentra el archivo
            ftp.cwd("/")
            if destino is None:
                destino = os.path.basename(archivo)

            # Definir el archivo local donde se guardará el archivo descargado
            with open(destino, 'wb') as archivo_local:
                ftp.retrbinary('RETR ' + archivo, archivo_local.write)
        print(
            f"Descargado archivo via FTP: {archivo} ")
    except Exception as e:
        print(f"Error al descargar via ftp: {e}")


def listar_ftp():
    hostname = "ftp.dlptest.com"
    username = "dlpuser"
    password = "rNrKYTX9g7z3RgJRmxWuGHbeu"

    # Conectar al servidor FTP
    with ftplib.FTP(hostname, username, password) as ftp:

        # Cambiar al directorio deseado
        ftp.cwd("/")

        # Listar el contenido del directorio
        contenido = ftp.nlst()

        # Imprimir el contenido del directorio
        for elemento in contenido:
            print(elemento)


def registrar_transferencia(hostname, archivo):
    logger.log(
        f"Transferencia a Host {hostname} de '{archivo}' ", "ftp", logging.INFO)

