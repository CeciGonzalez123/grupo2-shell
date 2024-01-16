import logging
import os


def log(message, log_type, level=logging.INFO):
    """
    Registra mensaje en logs según el tipo indicado.
    :param message: Mensaje para registrar en el log.
    :param log_type: Tipo de log, que también define el nombre del archivo de log.
    :param level: Nivel de log (INFO, ERROR, WARNING, etc.).
    """

    # Directorio de logs
    log_dir = "/var/log/shell"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Ruta del archivo de log
    log_file = os.path.join(log_dir, f"{log_type}.log")

    # Crea una instancia del objeto logging
    logger = logging.getLogger(log_type)

    # Configura el nivel de log si aún no está configurado
    if not logger.handlers:
        logger.setLevel(level)

        # Crea un manejador de archivos y lo añade al logger
        handler = logging.FileHandler(log_file)
        handler.setLevel(level)

        # Establece formato del log
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    # Registra el mensaje
    if level == logging.INFO:
        logger.info(message)
    elif level == logging.ERROR:
        logger.error(message)
    elif level == logging.WARNING:
        logger.warning(message)
    elif level == logging.DEBUG:
        logger.debug(message)
    else:
        raise ValueError("Nivel de log no válido")