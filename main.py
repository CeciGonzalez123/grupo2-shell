import os
import signal
from ftp import transferir_ftp
import logger
import logging
from comandos import (copiar_archivos, mover_archivos, renombrar_archivo,
                      listar_directorio, crear_directorios, cambiar_directorio,
                      cambiar_permisos, cambiar_propietario, cambiar_clave,
                      mostrar_directorio_actual, agregar_usuario,
                      matar_procesos, buscar_en_archivo, iniciar_demonio,
                      detener_demonio, ejecutar_comando_sistema)
# Lista para almacenar el historial de comandos de la sesión actual
historial_comandos = []


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

def obtener_pid_actual():
    # Función para obtener y mostrar el PID del proceso actual
    pid = os.getpid()
    print(f"El PID del proceso actual (shell.py) es: {pid}")


# Llamar a la función para mostrar el PID
obtener_pid_actual()




def registrar_comando(comando):
    # Función para registrar un comando en el historial
    historial_comandos.append(comando)


def mostrar_historial():
    # Función para mostrar el historial de comandos
    for num_linea, comando in enumerate(historial_comandos, 1):
        print(f"{num_linea}: {comando}")

def ejecutar_comando(comando):
    """
    Función para ejecutar un comando de la shell según el input del usuario
    """
    # Registra el comando en el historial
    registrar_comando(comando)
     # Registrar logs de accion
    logger.log(str(comando), "accion", logging.INFO)
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
    elif partes[0] == "permisos":
        # Invoca cambiar_permisos con una ruta y un modo
        if len(partes) == 3:
            ruta, modo = partes[1], partes[2]
            cambiar_permisos(ruta, modo)
        else:
            print("Error: El comando 'permisos' requiere dos argumentos (ruta y modo)")
    elif partes[0] == "propietario":
        # Invoca cambiar_propietario a multiples archivos
        if len(partes) > 1:
            cambiar_propietario(partes[1:])
        else:
            print(
                "Error: El comando 'propietario' requiere dos argumentos (ruta y 'usuario:grupo')")
    elif partes[0] == "clave":
        # Invoca cambiar_clave para usuario actual
        username = input("Introduzca el nombre de usuario: ")
        cambiar_clave(username)
    elif partes[0] == "actual":
        mostrar_directorio_actual()
    elif partes[0] == "usuario":
        username = input("Introduzca el nombre de usuario: ")
        agregar_usuario(username)
    elif partes[0] == "salir":
        exit()
    elif partes[0] == "matar":
        # Invoca matar_procesos con un pid y una señal
        # Ejemplo de uso: matar 1234 SIGKILL o SIGTERM
        if len(partes) >= 3:
            pids = partes[1:-1]
            senal_str = partes[-1]
            try:
                # Convierte el nombre de la señal a su correspondiente valor numérico
                if senal_str.startswith('SIG'):
                    senal = getattr(signal, senal_str)
                else:
                    senal = int(senal_str)
            except (AttributeError, ValueError):
                print("Señal no válida")
                return

            matar_procesos(pids, senal)
        else:
            print("Uso: matar PID(s) señal")
    elif partes[0] == "buscar":
        # Invoca buscar_en_archivo con un archivo y una cadena de búsqueda
        if len(partes) >= 3:
            archivo = partes[1]
            cadena_busqueda = " ".join(partes[2:])
            buscar_en_archivo(archivo, cadena_busqueda)
        else:
            print("Uso: buscar [archivo] [cadena de búsqueda]")
    elif comando.split()[0] == "historial":
        # Invoca mostrar_historial
        mostrar_historial()
    elif partes[0] == "demonio":
        # Invoca iniciar_demonio o detener_demonio
        if len(partes) >= 2:
            accion = partes[1]
            if accion == "iniciar":
                iniciar_demonio()
            elif accion == "detener":
                detener_demonio()
            else:
                print("Acción no reconocida. Use 'iniciar' o 'detener'.")
        else:
            print("Uso: demonio [iniciar/detener]")
    elif partes[0] == "ejecutar":
        # Invoca ejecutar_comando_sistema con el comando a ejecutar
        comando_sistema = " ".join(partes[1:])
        ejecutar_comando_sistema(comando_sistema)
    elif partes[0] == "transferir":
        # Invoca transferir_ftp con los parámetros necesarios
        if len(partes) >= 5:
            hostname = partes[1]
            username = partes[2]
            password = partes[3]
            archivo = partes[4]
            destino = partes[5] if len(partes) > 5 else '/'
            transferir_ftp(hostname, username, password, archivo, destino)
        else:
            print(
                "Uso: transferir [hostname] [username] [password] [archivo] [destino]")
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