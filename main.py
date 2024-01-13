import os
from comandos import (copiar_archivos)


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
       
    else: #escribis otra cosa que no esta programada
        print("Comando no reconocido")


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