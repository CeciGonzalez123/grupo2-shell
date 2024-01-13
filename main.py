import os

def mostrar_prompt():
    prompt = "Shell"
    """
    Imprime el valor de la variable prompt seguido de >,
    todo en una nueva línea, y mantiene el cursor en la misma línea 
    para que el usuario pueda introducir su entrada justo después del >.
    """
    print(f"\n{prompt}> ", end="")

def ejecutar_comando(comando):
    partes = comando.split()
    if partes[0] == "copiar":
        # Todo: Implementar copiar archivos
        print("Copiando archivos..")
    else:
        print("Comando no reconocido")


def main():
    print("Bienvenido al Shell Personalizado")
    print("Comandos disponibles:\n1. Copiar archivos")

    while True:
        mostrar_prompt()
        comando = input()
        ejecutar_comando(comando)


if __name__ == "__main__":
    main()