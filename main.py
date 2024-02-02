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
from datetime import datetime
import socket

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


def hora_actual():
    hora = datetime.now().strftime("%H:%M:%S")
    return datetime.strptime(hora, "%H:%M:%S").time()


def log_entrada(ip="127.0.1.1"):
    hora = hora_actual()
    ip_actual = socket.gethostbyname(ip)
    logger.log(
        f"Inicio de sesión a las '{hora}' desde la ip '{ip_actual}'.", "accion", logging.INFO)


def log_salida():
    hora = hora_actual()
    logger.log(
        f"Cierre de sesión a las '{hora}'", "accion", logging.INFO)


def ejecutar_comando(comando):
    """
    Función para ejecutar un comando de la shell según el input del usuario
    """
    # Registra el comando en el historial
    registrar_comando(comando)
    # Registrar logs de accion
    logger.log(str(comando), "accion", logging.INFO)
    partes = comando.split()
    if partes[0] == "copiar":
       # Invoca copiar_archivos con múltiples archivos de origen y un destino
        if len(partes) >= 3:
            *origenes, destino = partes[1:]
            copiar_archivos(origenes, destino)
        else:
            print(
                "Uso: copiar [archivo_1] [archivo_2] [archivo_n] [ruta_destino]")
    elif partes[0] == "mover":
        # Invoca mover_archivos con múltiples archivos de origen y un destino
        if len(partes) >= 3:
            *origenes, destino = partes[1:]
            mover_archivos(origenes, destino)
        else:
            print(
                "Uso: mover [archivo_1] [archivo_2] [archivo_n] [ruta_destino]")
    elif partes[0] == "renombrar":
        # Invoca renombrar_archivo con 2 parámetros
        if len(partes) == 3:
            origen, nuevo_nombre = partes[1], partes[2]
            renombrar_archivo(origen, nuevo_nombre)
        else:
            print("Uso: renombrar [archivo] [nuevo_nombre]")
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
            print("Uso: creardir [directorio_1] [directorio_2] [directorio_n]")
    elif partes[0] == "ir":
        # Invoca cambiar_directorio con a la ruta indicada en el parametro
        if len(partes) == 2:
            destino = partes[1]
            cambiar_directorio(destino)
        else:
            print("Uso: ir [ruta_destino]")
    elif partes[0] == "permisos":
        # Invoca cambiar_permisos con una ruta y un modo
        if len(partes) == 3:
            ruta, modo = partes[1], partes[2]
            cambiar_permisos(ruta, modo)
        else:
            print("Uso: permisos [archivo] [modo]")
    elif partes[0] == "propietario":
        # Invoca cambiar_propietario a multiples archivos y los asigna al usuario root
        if len(partes) > 1:
            cambiar_propietario(partes[1:])
        else:
            print(
                "Uso: propietario [archivo_1] [archivo_2] [archivo_n]")
    elif partes[0] == "clave":
        # Invoca cambiar_clave para usuario actual
        if len(partes) == 1:
            username = input("Introduzca el nombre de usuario: ")
            cambiar_clave(username)
        else:
            print("Uso: clave")
    elif partes[0] == "actual":
        # Invoca mostrar_directorio_actual
        if len(partes) == 1:
            mostrar_directorio_actual()
        else:
            print("Uso: actual")
    elif partes[0] == "usuario":
        # Invoca agregar_usuario con un nombre de usuario
        if len(partes) == 1:
            username = input("Introduzca el nombre de usuario: ")
            agregar_usuario(username)
        else:
            print("Uso: usuario")
    elif partes[0] == "salir":
        # Registra log de entrada y sale del programa
        if len(partes) == 1:
            log_salida()
            exit()
        else:
            print("Uso: salir")
    elif partes[0] == "matar":
        # Invoca matar_procesos con un pid
        # Ejemplo de uso: matar 1234
        if len(partes) == 2:
            pid = partes[1]
            matar_procesos(pid)
        else:
            print("Uso: matar [PID]")
    elif partes[0] == "buscar":
        # Invoca buscar_en_archivo con un archivo y una cadena de búsqueda
        if len(partes) >= 3:
            archivo = partes[1]
            cadena_busqueda = " ".join(partes[2:])
            buscar_en_archivo(archivo, cadena_busqueda)
        else:
            print(len(partes))
            print("Uso: buscar [archivo] [cadena de búsqueda]")
    elif partes[0] == "historial":
        # Invoca mostrar_historial
        if len(partes) == 1:
            mostrar_historial()
        else:
            print("Uso: historial")
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
        # Invoca mostrar_directorio_actual
        if len(partes) > 1:
            comando_sistema = " ".join(partes[1:])
            ejecutar_comando_sistema(comando_sistema)
        else:
            print("Uso: ejecutar [comando]")
    elif partes[0] == "transferir":
        # Invoca transferir_ftp con los parámetros necesarios
        if len(partes) == 5:
            hostname = partes[1]
            username = partes[2]
            password = partes[3]
            archivo = partes[4]
            transferir_ftp(hostname, username, password, archivo)
        else:
            print(
                "Uso: transferir [hostname] [username] [password] [archivo]")
    else:  # Si usuario ingresa un comando no reconocido
        print("Comando no reconocido")


def main():
    """
    Ciclo que siempre esta abierto mientras sea verdadero
    """

    # Registra log de inicio de sesión
    log_entrada()

    while True:
        mostrar_prompt()  # muestra el prompt
        comando = input()  # variable que recibe el input del usuario: comando y parametros
        ejecutar_comando(comando)  # llamamos a ejecutar_comando


if __name__ == "__main__":
    main()

