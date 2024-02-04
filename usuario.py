import getpass
import re
import pwd
import os
import json


def validar_usuario(usuario):
    """Validar nombre de usuario y verificar si usuario existe.
    Retorna True si el nombre de usuario es válido y no existe en el sistema.
    """
    # Primero, validar el patrón del nombre de usuario
    if re.match("^[a-z]+$", usuario) is None:
        print(f"El nombre de usuario {usuario} es inválido.")
        return False

    # Luego, verificar si el usuario ya existe en el sistema
    try:
        pwd.getpwnam(usuario)
        # Si se encuentra el usuario, significa que ya existe, retornar False
        print(f"El usuario {usuario} ya existe.")
        return False
    except KeyError:
        # Si se lanza KeyError, el usuario no existe, lo cual es bueno en este contexto
        return True


def validar_ip(ip):
    patron_ip = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    if patron_ip.match(ip):
        partes_ip = ip.split('.')
        return all(0 <= int(part) <= 255 for part in partes_ip)
    return False


def validar_hora(hora):
    patron_hora = re.compile(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
    return bool(patron_hora.match(hora))


def solicitar_datos():
    print("El nombre de usuario debe contener solo caracteres válidos 'a-z'")

    while True:
        usuario = input("Ingrese nombre de usuario: ")
        if validar_usuario(usuario):
            break
        else:
            print("Error, intente nuevamente.")

    while True:
        entrada = input("Ingrese la hora de entrada (HH:MM): ")
        if validar_hora(entrada):
            break
        else:
            print("Hora de entrada inválida. Por favor, use el formato HH:MM (24 horas).")

    while True:
        salida = input("Ingrese la hora de salida (HH:MM): ")
        if validar_hora(salida) and entrada < salida:
            break
        else:
            print(
                "Hora de salida inválida o anterior a la hora de entrada. Por favor, revise los valores.")

    while True:
        ip = input("Ingrese la dirección IP: ")
        if validar_ip(ip):
            break
        else:
            print("Dirección IP inválida. Por favor, ingrese una dirección IP válida.")

    return [usuario, entrada, salida, ip]


def ingresar_clave():
    print(
        "La clave debe contener al menos: una letra en minuscula, un numero un simbolo y un minimo de 8 caracteres")

    while True:
        passy = getpass.getpass(prompt="Ingrese password para el usuario: ")
        confirm_passy = getpass.getpass(prompt="Confirme password: ")

        # Verificar:
        # coincidencia de password y confirmacion
        # longitud de al menos 8 caracteres
        # clave contiene al menos 1 numero
        # clave contiene al menos 1 letra
        # clave contiene al menos 1 simbolo

        if passy != confirm_passy \
                or len(passy) < 8 \
                or not re.search('\d', passy) \
                or not re.search(r"[a-z]", passy) \
                or not re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', passy):

            print("Clave no permitida, intente nuevamente")
            continue

        else:
            return passy


def agregar_usuario():
    datos = solicitar_datos()
    code = ingresar_clave()
    usuario = datos[0]

    os.system(
        f"useradd --create-home --user-group --shell /bin/bash {usuario}")
    os.system(f"echo {usuario}:{code} | chpasswd")

    # Datos adicionales
    metadata = {
        'entrada': datos[1],
        'salida': datos[2],
        'ip': datos[3]
    }

    # Guardar los datos adicionales en un archivo JSON en el directorio home del usuario
    home_dir = f"/home/{usuario}"
    metadata_file = os.path.join(home_dir, f"{usuario}_metadata.json")

    with open(metadata_file, 'w') as file:
        json.dump(metadata, file)

    print(
        f"Usuario {usuario} creado con éxito. Información adicional almacenada en {metadata_file}.")


def cambiar_clave(usuario):
    print(f"Cambiando la contraseña de: {usuario}")

    while True:
        nueva_password = getpass.getpass(
            prompt="Ingrese la nueva contraseña: ")
        confirmar_password = getpass.getpass(
            prompt="Confirme la nueva contraseña: ")

        # Verificar:
        # coincidencia de password y confirmacion
        # longitud de al menos 8 caracteres
        # clave contiene al menos 1 numero
        # clave contiene al menos 1 letra
        # clave contiene al menos 1 simbolo
        if nueva_password != confirmar_password:
            print("Las contraseñas no coinciden. Intente de nuevo.")
        elif len(nueva_password) < 8:
            print("La contraseña debe tener al menos 8 caracteres.")
        elif not re.search('\d', nueva_password):
            print("La contraseña debe contener al menos un número.")
        elif not re.search(r"[a-z]", nueva_password):
            print("La contraseña debe contener al menos una letra minúscula.")
        elif not re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', nueva_password):
            print("La contraseña debe contener al menos un símbolo.")
        else:
            break  # La contraseña es válida y coincide

    # Cambiar la contraseña del usuario
    os.system(f"echo '{usuario}:{nueva_password}' | sudo chpasswd")
    print(f"Contraseña cambiada exitosamente para el usuario {usuario}.")


def leer_metadata_usuario(usuario):
    # Ubicación del archivo de metadata basada en el nombre del usuario
    home_dir = f"/home/{usuario}"
    metadata_file = os.path.join(home_dir, f"{usuario}_metadata.json")

    # Verificar si el archivo existe
    if os.path.exists(metadata_file):
        # Leer y deserializar el contenido del archivo JSON
        with open(metadata_file, 'r') as file:
            metadata = json.load(file)
            return metadata
    else:
        return {}
