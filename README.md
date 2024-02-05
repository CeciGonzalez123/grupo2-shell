 ## Documentacion Shell
 ### Manual de instalacion 

<p>Pasos a seguir</p>


1. Desde el ubuntu entrar como usuario root
2. Ejecutar el comando export LFS=/mnt/lfs
3. Ejecutar el comando cd $LFS 
4. Ejecutar el comando ls para comprobar si se encuentra /sources
1. Ejecutar el comando cd /sources y crear directorio con el nombre del directorio de la shell (en nuestro caso grupo2-shell)
2.Ejecutar el comando ls para comprobar el contenido de /sources
3. Entrar al lfs como usuario root, en en el lfs el directorio / equivale a /mnt/lfs,hacer pwd para comprobar que estamos en la /
4. Ejecutar el comando cd /sources, para movernos al directorio /sources
1. Ejecutar el comando pwd para comprobar el contenido de /sources
2. Ejecutar el comando cd grupo2-shell y ejecutar git https://github.com/CeciGonzalez123/grupo2-shell, con eso clonamos el repositorio dentro del lfs
3. ejecutamos python3 main.py para entrar dentro de la shell manualmente y ejecutamos el comando copiar /sources/grupo2-shell / para mover el repositorio a /
4. salimos de la shell con el comando salir
1. cd / para movernos a al directorio /
2. ejecutamos chmod -R 777/grupo2-shell 
3. ls -l para comprobar si le dio todos los permisos
4. Entrar al ubuntu, ejecutar export LFS=/mnt/lfs y cd $LFS
1. Ejecutar sudo nano /etc/profile, borrar el contenido 
2. Ejecutar sudo nano shell.sh, agregarle el script:  
#!/bin/bash
      cd /grupo2-shell
      python3 main.py
3. ejecutamos sudo nano /etc/profile, agregarle el script:
      bash /shell.sh
4. Como usuario root ejecutar  chmod -R 777 var/log/shell
### Instrucciones de uso comandos Shell
 #### COPIAR
 <p>Uso: copiar [archivo_1] [archivo_2] [archivo_n] [ruta_destino]</p>
 <p>Copia múltiples archivos o directorios de origen a un destino</p>

#### MOVER
<p>Uso: mover [archivo_1] [archivo_2] [archivo_n] [ruta_destino]</p>
 <p>Mueve múltiples archivos o directorios de origen a un destino</p>

#### RENOMBRAR
<p>Uso: renombrar [archivo] [nuevo_nombre]</p>
 <p>Renombra un archivo o una carpeta.</p>

 #### LISTAR
 <p>Uso: listar </p>
 <p>Lista el directorio actual.</p>

 #### CREARDIR
 <p>Uso: creardir [directorio_1] [directorio_2] [directorio_n] </p>
 <p>Crea uno o multiples directorios.</p>

 #### IR
 <p>Uso: ir [ruta_destino] </p>
 <p>Cambia al directorio especificado en el parametro</p>

 #### PERMISOS
 <p>permisos [archivo] [modo] </p>
 <p>Cambia los permisos de un archivo o directorio</p>

 #### PROPIETARIO
 <p>Uso: propietario [archivo_1] [archivo_2] [archivo_n] [usuario:grupo]</p>
 <p>Asigna el usuario:grupo indicado a uno o multiples archivos o directorios,</p>

#### CLAVE
<p>Uso: clave </p>
 <p>Cambia la contraseña del usuario que le especifiques</p>

#### ACTUAL
<p>Uso: actual </p>
<p>Muestra el directorio actual </p>

#### USUARIO
<p>Uso: usuario </p>
<p>Agrega un nuevo usuario </p>
<p> Cuando se ejecute, ingresar los siguientes datos:</p>
<p>1.	Ingrese nombre de usuario:</p>
<p>2.	Ingrese la hora de entrada (HH:MM):</p>
<p>3.	Ingrese la hora de salida (HH:MM):</p>
<p>4.	Ingrese la dirección IP </p>
<p>5.	Ingrese password para el usuario: </p>

#### MATAR
<p>Uso: matar [PID] </p>
<p> Finaliza el proceso con el PID especificado</p>

#### BUSCAR
<p>Uso: buscar [archivo] [cadena de búsqueda] </p>
<p> Busca un palabra/cadena en el archivo especificado </p>

#### HISTORIAL
<p>Uso: historial</p>
<p>Muestra el historial de comandos utilizados</p>

#### EJECUTAR
<p>Uso: ejecutar [comando]</p>
<p>Ejecuta comandos externos a la shell</p>

#### DEMONIO
<p>Uso: demonio [iniciar/detener]</p>
<p>Detiene o inicia un subproceso</p>cadena en el archivo 

#### FTP
<p>Uso: ftp</p>
<p>Lista archivos del servidor ftp de prueba ftp</p>

#### DESCARGAR
<p>Uso: descargar [archivo]</p>
<p>Descarga archivos del servidor ftp de prueba</p>

#### TRANSFERIR
<p>Uso: transferir [archivo]</p>
<p>Transifiere el archivo especificado al servidor ftp de prueba</p>






