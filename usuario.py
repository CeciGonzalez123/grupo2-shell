import getpass
import re
import pwd
import crypt
import json
import os
from pathlib import Path
import spwd  # Para verificar si el usuario ya existe en /etc/shadow


def obtener_uid_gid_siguiente():
    # Esto es una simplificación. En un sistema real, se deberían verificar los UID/GID existentes para evitar colisiones.
    uid_base = 1000
    gid_base = 1000
    max_uid = uid_base
    max_gid = gid_base
    try:
        with open("/etc/passwd", "r") as f:
            for line in f:
                parts = line.split(":")
                if int(parts[2]) > max_uid:
                    max_uid = int(parts[2])
                if int(parts[3]) > max_gid:
                    max_gid = int(parts[3])
    except FileNotFoundError:
        pass  # /etc/passwd no encontrado, usar valores base
    return max_uid + 1, max_gid + 1


def validar_usuario(usuario):
    if re.match("^[a-z]+$", usuario) is None:
        print(f"El nombre de usuario {usuario} es inválido.")
        return False
    try:
        pwd.getpwnam(usuario)
        print(f"El usuario {usuario} ya existe.")
        return False
    except KeyError:
        # También verificar en /etc/shadow por seguridad
        try:
            spwd.getspnam(usuario)
            print(f"El usuario {usuario} ya existe en /etc/shadow.")
            return False
        except KeyError:
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
    print("La clave debe contener al menos: una letra minúscula, un número, un símbolo y un mínimo de 8 caracteres.")
    while True:
        clave = getpass.getpass(prompt="Ingrese password para el usuario: ")
        confirmacion_clave = getpass.getpass(prompt="Confirme password: ")
        if (clave == confirmacion_clave and len(clave) >= 8 and re.search(r"\d", clave) and
                re.search(r"[a-z]", clave) and re.search(r"[!@#$%^&*(),.?\":{}|<>]", clave)):
            return clave
        else:
            print("Clave no permitida, intente nuevamente.")


def encriptar_clave(clave):
    salt = crypt.mksalt(crypt.METHOD_SHA512)
    return crypt.crypt(clave, salt)


def agregar_usuario(usuario, clave, uid, gid):
    clave_encriptada = crypt.crypt(clave, crypt.mksalt(crypt.METHOD_SHA512))

    # Crear grupo
    with open("/etc/group", "a") as group_file:
        group_file.write(f"{usuario}:x:{gid}:\n")

    # Crear usuario y corregir el formato de GECOS
    home_dir = f"/home/{usuario}"
    shell = "/bin/bash"
    with open("/etc/passwd", "a") as passwd_file:
        passwd_file.write(f"{usuario}:x:{uid}:{gid}::{home_dir}:{shell}\n")

    # Configurar contraseña
    with open("/etc/shadow", "a") as shadow_file:
        shadow_file.write(f"{usuario}:{clave_encriptada}:17646:0:99999:7:::\n")

    # Crear directorio home y establecer permisos y propiedad
    os.makedirs(home_dir, exist_ok=True)
    os.system(f"chown {uid}:{gid} {home_dir}")
    os.system(f"chmod 700 {home_dir}")


def crear_usuario():
    datos = solicitar_datos()
    clave = ingresar_clave()
    usuario = datos[0]
    uid, gid = obtener_uid_gid_siguiente()
    clave_encriptada = encriptar_clave(clave)
    agregar_usuario(usuario, clave, uid, gid)

    metadata_file = Path(f"/home/{usuario}") / f"{usuario}_metadata.json"
    with metadata_file.open('w') as file:
        json.dump({
            'entrada': datos[1],
            'salida': datos[2],
            'ip': datos[3]
        }, file)
    print(
        f"Usuario {usuario} creado con éxito. Información adicional almacenada en {metadata_file}.")


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


def cambiar_clave(usuario):
    if validar_usuario(usuario):
        print(f"El usuario {usuario} no existe.")
        return

    print(f"Cambiando la contraseña de: {usuario}")

    while True:
        nueva_password = getpass.getpass(
            prompt="Ingrese la nueva contraseña: ")
        confirmar_password = getpass.getpass(
            prompt="Confirme la nueva contraseña: ")

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

    clave_encriptada = encriptar_clave(nueva_password)

    # Leer /etc/shadow, encontrar la línea del usuario, y actualizar la contraseña
    try:
        with open("/etc/shadow", "r") as shadow_file:
            lineas = shadow_file.readlines()

        with open("/etc/shadow", "w") as shadow_file:
            for linea in lineas:
                if linea.startswith(usuario + ":"):
                    partes = linea.split(":")
                    # Actualizar la contraseña encriptada
                    partes[1] = clave_encriptada
                    linea = ":".join(partes)
                shadow_file.write(linea)

        print(f"Contraseña cambiada exitosamente para el usuario {usuario}.")
    except FileNotFoundError:
        print("No se pudo encontrar el archivo /etc/shadow.")
    except PermissionError:
        print("No se tienen los permisos necesarios para modificar /etc/shadow. Se requiere ejecutar como root.")
