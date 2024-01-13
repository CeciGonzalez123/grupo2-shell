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