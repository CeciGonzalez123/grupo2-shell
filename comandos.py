import shutil
import os
import signal
import stat
import pwd
import grp
import subprocess
from pathlib import Path
from demonio import Demonio
import logger
import logging

demonio = None


def copiar_archivos(origenes, destino):
    """
    Copia uno o múltiples archivos de 'origenes' a 'destino'.
    :param origenes: Lista de rutas de archivos a copiar.
    :param destino: Ruta de destino donde se copiarán los archivos.
    """
    try:
        for origen in origenes:  # origenes es una lista de elementos y recorre eso
            if os.path.isdir(origen):
                shutil.copytree(origen, os.path.join(
                    destino, os.path.basename(origen)))
            else:
                shutil.copy(origen, destino)
        print(f"\nArchivos copiados correctamente a '{destino}'.\n")
    except Exception as e:  # manda las excepciones a la variable e
        logger.log(
            f"Error al copiar: {e}",
            "sistema_error",
            logging.ERROR)
        print(f"Error al copiar: {e}")


def mover_archivos(origenes, destino):
    """
    Mueve múltiples archivos de 'origenes' a 'destino'.
    :param origenes: Lista de rutas de archivos a mover.
    :param destino: Ruta de destino donde se moverán los archivos.
    """
    try:
        for origen in origenes:
            # Destino final para cada archivo/directorio
            destino_final = os.path.join(destino, os.path.basename(origen))

            # Mover archivo o directorio
            shutil.move(origen, destino_final)

        print(f"\nArchivos movidos correctamente a '{destino}'.\n")
    except Exception as e:
        logger.log(
            f"Error al mover: {e}",
            "sistema_error",
            logging.ERROR)
        print(f"Error al mover: {e}")


def renombrar_archivo(origen, nuevo_nombre):
    """
    Renombra un archivo o directorio.
    :param origen: Ruta del archivo o directorio a renombrar.
    :param nuevo_nombre: Nuevo nombre para el archivo o directorio.
    """
    try:
        # Extraemos el directorio base donde se encuentra el archivo
        base_dir = os.path.dirname(origen)
        destino = os.path.join(base_dir, nuevo_nombre)
        # Renombramos el archivo o directorio
        os.rename(origen, destino)
        print(f"\n'{origen}' ha sido renombrado a '{destino}'.\n")
    except FileNotFoundError:
        logger.log(
            f"El archivo {origen} no existe.",
            "sistema_error",
            logging.ERROR)
        print(f"El archivo {origen} no existe.")
    except Exception as e:
        logger.log(
            f"Error al renombrar: {e}",
            "sistema_error",
            logging.ERROR)
        print(f"Error al renombrar: {e}")


def listar_directorio(ruta='.'):
    """
    Lista los archivos y directorios de la ruta dada o del directorio actual si no se especifica una ruta.
    :param ruta: Ruta del directorio a listar.
    """
    try:
        # Listar el contenido del directorio
        with os.scandir(ruta) as entradas:
            for entrada in entradas:
                print(f"   {entrada.name}")
    except Exception as e:
        logger.log(
            f"Error al listar directorio: {e}",
            "sistema_error",
            logging.ERROR)
        print(f"Error al listar directorio: {e}")


def crear_directorios(directorios):
    """
    Crea uno o varios directorios.
    :param directorios: Lista de nombres de directorios a crear.
    """
    try:
        for directorio in directorios:
            os.makedirs(directorio, exist_ok=False)
            print(f"Directorio '{directorio}' creado con éxito.")
    except Exception as e:
        logger.log(
            f"Error al crear directorios: {e}",
            "sistema_error",
            logging.ERROR)
        print(f"Error al crear directorios: {e}")


def cambiar_directorio(destino):
    """
    Cambia el directorio de trabajo actual al directorio especificado.
    :param destino: Ruta del directorio de destino.
    """
    try:
        # Verificar si el archivo o directorio existe
        if not os.path.exists(destino):
            raise FileNotFoundError(
                f"El archivo o directorio '{destino}' no existe.")
        os.chdir(destino)
        print(f"Directorio cambiado a '{destino}'")
    except Exception as e:
        logger.log(
            f"Error al cambiar de directorio: {e}",
            "sistema_error",
            logging.ERROR)
        print(f"Error al cambiar de directorio: {e}")


def cambiar_permisos(ruta, modo):
    """
    Cambia los permisos de un archivo o directorio.
    :param ruta: Ruta del archivo o directorio cuyos permisos se cambiarán.
    :param modo: Modo de permiso en formato octal (ejemplo: '755').
    """
    try:
        # Verificar si el archivo o directorio existe
        if not os.path.exists(ruta):
            raise FileNotFoundError(
                f"El archivo o directorio '{ruta}' no existe.")
        # Convertir el modo de string a formato octal
        modo_octal = int(modo, 8)
        os.chmod(ruta, modo_octal)
        print(f"Permisos de '{ruta}' cambiados a {modo}")
    except FileNotFoundError:
        logger.log(
            f"El archivo {ruta} no existe.",
            "sistema_error",
            logging.ERROR)
        print(f"El archivo {ruta} no existe.")
    except Exception as e:
        logger.log(
            f"Error al cambiar permisos: {e}",
            "sistema_error",
            logging.ERROR)
        print(f"Error al cambiar permisos: {e}")


def cambiar_propietario(archivos, propietario):
    """
    Cambia los propietarios de un archivo o un conjunto de archivos.
    :param archivos: Lista de rutas de archivos o directorios cuyos propietarios se cambiarán.
    :param propietario: usuario:grupo al que se cambiará el propietario.
    """

    ids = propietario.split(':')
    uid = ids[0]
    gid = ids[1]

    try:
        # Obtener el UID del nombre de usuario
        uid_int = pwd.getpwnam(uid).pw_uid

        # Obtener el GID del nombre de grupo
        gid_int = grp.getgrnam(gid).gr_gid

        for archivo in archivos:
            if not os.path.exists(archivo):
                raise FileNotFoundError(
                    f"El archivo o directorio '{archivo}' no existe.")

            # Cambiar el propietario del archivo
            os.chown(archivo, uid_int, gid_int)
            print(f"Propietario de '{archivo}' cambiado a {uid}:{gid}")

    except KeyError:
        print(f"El usuario '{uid}' o el grupo '{gid}' no existen.")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Error al cambiar propietario: {e}")
        logger.log(
            f"Error al cambiar propietario: {e}",
            "sistema_error",
            logging.ERROR)


def mostrar_directorio_actual():
    """
    Muestra el directorio de trabajo actual.
    """
    try:
        print(f"Directorio actual: {Path.cwd()}")
    except Exception as e:
        logger.log(
            f"Error al obtener el directorio actual: {e}",
            "sistema_error",
            logging.ERROR)
        print(f"Error al obtener el directorio actual: {e}")


def matar_procesos(pid):
    """
    Termina proceso enviando una señal específica.
    :param pid: PID del proceso a terminar.    
    """
    try:
        os.kill(int(pid), signal.SIGKILL)
        print(f"Proceso con PID {pid} ha sido terminado.")
    except ProcessLookupError:
        print(f"No se encontró el proceso con PID {pid}.")
        logger.log(
            f"No se encontró el proceso con PID {pid}",
            "sistema_error",
            logging.ERROR)
    except Exception as e:
        print(f"Error al enviar señal: {e}")
        logger.log(
            f"Error al enviar señal: {e}",
            "sistema_error",
            logging.ERROR)


def buscar_en_archivo(archivo, cadena_busqueda):
    """
    Busca una cadena de texto en un archivo y muestra las líneas que la contienen.
    :param archivo: Ruta del archivo donde buscar.
    :param cadena_busqueda: Cadena de texto a buscar en el archivo.
    """
    try:
        with open(archivo, 'r') as file:
            for num_linea, linea in enumerate(file, 1):
                if cadena_busqueda.lower() in linea.lower():
                    print(f"Línea {num_linea}: {linea.strip()}")

    except FileNotFoundError:
        logger.log(
            f"El archivo {archivo} no existe.",
            "sistema_error",
            logging.ERROR)
        print(f"El archivo {archivo} no existe.")
    except Exception as e:
        logger.log(
            f"Error al buscar en el archivo: {e}",
            "sistema_error",
            logging.ERROR)
        print(f"Error al buscar en el archivo: {e}")


def iniciar_demonio():
    global demonio
    if demonio is None or not demonio.is_alive():
        demonio = Demonio()
        demonio.start()
    else:
        print("El demonio ya está en ejecución.")


def detener_demonio():
    global demonio
    if demonio is not None and demonio.is_alive():
        demonio.detener()
        demonio.join()
    else:
        print("El demonio no está activo.")


def ejecutar_comando_sistema(comando):
    comandos_implementados = {
        'cp': 'copiar',
        'mv': 'mover',
        'historial': 'history',
        'creadir': 'mkfir',
        'chmod': 'permisos',
        'chown': 'propietario',
        'grep': 'buscar',
        'pwd': 'actual',
        'cd': 'ir',
        'ls': 'listar',
        'clave': 'passwd',
        'matar': 'kill',
        'ftp': 'transferir',
    }

    if comando in comandos_implementados:
        print(
            f"El comando '{comando}' ya está implementado como '{comandos_implementados[comando]}'.")
    else:
        try:
            resultado = subprocess.run(comando, shell=True, check=True,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(resultado.stdout)
            if resultado.stderr:
                print(resultado.stderr)
        except subprocess.CalledProcessError as e:
            logger.log(
                f"Error al ejecutar el comando del sistema: {e}",
                "sistema_error",
                logging.ERROR)
            print(f"Error al ejecutar el comando del sistema: {e}")
