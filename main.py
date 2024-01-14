import os
from comandos import (copiar_archivos, mover_archivos, renombrar_archivo,
                      listar_directorio,crear_directorios,cambiar_directorio)


def mostrar_prompt():
    prompt = "Shell"
    """
    Imprime el valor de la variable prompt seguido de >,
    todo en una nueva línea, y mantiene el cursor en la misma línea 
    para que el usuario pueda introducir su entrada justo después del >.
    """
    print(f"\n{prompt}> ", end="")
    
    """
    ejemplo comando ="uno dos tres" y partes =comando.split(),
    entonces partes va a tener un array(lista) de 3 posiciones, el 1er elemento de
    la lista es el comando y los siguientes elementos son parametros, en el caso que
    tengas uno,dos,tres en el split envio entre parentesis (",") usando como parametro
    la coma que seria el separador
    """
def ejecutar_comando(comando):
    partes = comando.split()
    if partes[0] == "copiar": #compara
       # Invoca copiar_archivos con múltiples archivos de origen y un destino
        if len(partes) >= 3:
            *origenes, destino = partes[1:]
            copiar_archivos(origenes, destino)
        else:
            print("Error: Se necesitan al menos dos argumentos para 'copiar'")
    elif partes[0] == "mover":
        # Invoca mover_archivos con múltiples archivos de origen y un destino
        if len(partes) >= 3:
            *origenes, destino = partes[1:]
            mover_archivos(origenes, destino)
        else:
            print("Error: Se necesitan al menos dos argumentos para 'mover'")
   
    elif partes[0] == "renombrar":
        # Invoca renombrar_archivo con 2 parámetros
        if len(partes) == 3:
            origen, nuevo_nombre = partes[1], partes[2]
            renombrar_archivo(origen, nuevo_nombre)
        else:
            print("Error: El comando 'renombrar' requiere exactamente dos argumentos")
    elif partes[0] == "listar":
        # Invoca listar_directorio con un directorio (o el directorio actual)
        directorio = partes[1] if len(partes) > 1 else '.'
        listar_directorio(directorio)
    elif partes[0] == "creardir":
        # Invoca crear_directorios con múltiples directorios
        if len(partes) > 1:
            directorios = partes[1:]
            crear_directorios(directorios)
        else:
            print("Error: El comando 'creardir' requiere al menos un argumento")
    elif partes[0] == "ir":
        # Invoca cambiar_directorio con a la ruta indicada en el parametro
        if len(partes) == 2:
            destino = partes[1]
            cambiar_directorio(destino)
        else:
            print("Error: El comando 'ir' requiere un argumento de destino")

def main():
    """
    Ciclo que siempre esta abierto mientras sea verdadero
    """
    while True: 
        mostrar_prompt() #muestra el prompt
        comando = input() #variable que recibe el input del usuario, el comando y los parametros
        ejecutar_comando(comando) #llamamos a ejecutar_comando


if __name__ == "__main__":
    main()