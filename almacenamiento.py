"""
Lectura y escritura de los trámites en el archivo de texto local.

Formato del archivo tramites_samne.txt: una línea por trámite y 8 campos
separados por "|", en este orden:

    codigo|fecha_recepcion|dni|nombre|tipo|asunto|estado|fecha_entrega

Ejemplo:
    TRA-0001|30/04/2026|12345678|Diego Martinez|Permiso|Uso de cancha|PENDIENTE|-

El archivo contiene datos personales (DNI y nombres), por eso está incluido
en .gitignore y nunca se sube a GitHub.
"""

from validaciones import SEPARADOR

ARCHIVO = "tramites_samne.txt"
CANTIDAD_CAMPOS = 8


def cargar_datos(ruta: str = ARCHIVO) -> list[list[str]]:
    """
    Lee los trámites guardados en el archivo de texto.

    Si el archivo todavía no existe (primera ejecución), se empieza con una
    lista vacía. Las líneas dañadas (con un número de campos distinto de 8)
    se ignoran para que el programa no se detenga.

    Parámetros:
        ruta (str): ubicación del archivo; por defecto "tramites_samne.txt".

    Retorna:
        list[list[str]]: lista de trámites; cada trámite es una lista de
        8 textos.
    """
    tramites = []
    try:
        # "with" cierra el archivo automáticamente, incluso si ocurre un error
        with open(ruta, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                campos = linea.strip().split(SEPARADOR)
                if len(campos) == CANTIDAD_CAMPOS:
                    tramites.append(campos)
    except FileNotFoundError:
        pass  # primera ejecución: el archivo se crea al guardar
    return tramites


def guardar_datos(tramites: list[list[str]], ruta: str = ARCHIVO) -> None:
    """
    Escribe todos los trámites en el archivo, reemplazando su contenido.

    Parámetros:
        tramites (list[list[str]]): trámites a guardar.
        ruta (str): ubicación del archivo; por defecto "tramites_samne.txt".

    Retorna:
        None
    """
    with open(ruta, "w", encoding="utf-8") as archivo:
        for tramite in tramites:
            archivo.write(SEPARADOR.join(tramite) + "\n")
