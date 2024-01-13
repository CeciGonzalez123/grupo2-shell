import shutil
import os


def copiar_archivos(origenes, destino):
    """
    Copia uno o múltiples archivos de 'origenes' a 'destino'.
    :param origenes: Lista de rutas de archivos a copiar.
    :param destino: Ruta de destino donde se copiarán los archivos.
    """
    try:
        for origen in origenes: #origenes es una lista de elementos y recorre eso
            if os.path.isdir(origen):
                shutil.copytree(origen, os.path.join(
                    destino, os.path.basename(origen)))
            else:
                shutil.copy(origen, destino)
        print(f"\nArchivos copiados correctamente a '{destino}'.\n")
    except Exception as e: #manda las excepciones a la variable e
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
        print(destino)
        # Renombramos el archivo o directorio
        os.rename(origen, destino)
        print(f"\n'{origen}' ha sido renombrado a '{destino}'.\n")
    except Exception as e:
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
                print(entrada.name)
    except Exception as e:
        print(f"Error al listar directorio: {e}")
def crear_directorios(directorios):
    """
    Crea uno o varios directorios.
    :param directorios: Lista de nombres de directorios a crear.
    """
    try:
        for directorio in directorios:
            os.makedirs(directorio, exist_ok=True)
            print(f"Directorio '{directorio}' creado con éxito.")
    except Exception as e:
        print(f"Error al crear directorios: {e}")