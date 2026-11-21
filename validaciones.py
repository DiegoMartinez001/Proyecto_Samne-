"""
Validaciones de los datos ingresados por la secretaria.

Todas las funciones de este módulo son "puras": reciben datos y devuelven
True/False (o una fecha), sin leer del teclado ni imprimir en pantalla.
Por eso se pueden probar de forma automática (ver tests/test_validaciones.py).
"""

from datetime import date, datetime

FORMATO_FECHA = "%d/%m/%Y"   # dd/mm/aaaa, el formato que usa la municipalidad
LONGITUD_DNI = 8
SEPARADOR = "|"              # separador de campos en tramites_samne.txt
LONGITUD_MAXIMA_TEXTO = 100  # evita registros enormes que dificulten la lectura


def convertir_fecha(fecha_texto: str) -> date | None:
    """
    Convierte un texto con formato dd/mm/aaaa en una fecha.

    Parámetros:
        fecha_texto (str): fecha escrita por el usuario, p. ej. "30/04/2026".

    Retorna:
        date | None: la fecha convertida, o None si el texto no es una
        fecha real (por ejemplo "31/02/2026" o "hola").

    Ejemplo:
        >>> convertir_fecha("30/04/2026")
        datetime.date(2026, 4, 30)
    """
    try:
        return datetime.strptime(fecha_texto, FORMATO_FECHA).date()
    except ValueError:
        return None


def validar_fecha(fecha_texto: str) -> bool:
    """
    Indica si el texto corresponde a una fecha válida en formato dd/mm/aaaa.

    Parámetros:
        fecha_texto (str): fecha escrita por el usuario.

    Retorna:
        bool: True si la fecha existe en el calendario; False en caso contrario.
    """
    return convertir_fecha(fecha_texto) is not None


def validar_fecha_recepcion(fecha_texto: str, hoy: date | None = None) -> bool:
    """
    Valida la fecha en que la municipalidad recibió el documento.

    Regla de negocio: un documento no puede haberse recibido en el futuro.

    Parámetros:
        fecha_texto (str): fecha de recepción en formato dd/mm/aaaa.
        hoy (date | None): fecha de referencia. Si no se indica, se usa la
            fecha del sistema. Se recibe como parámetro para poder probar
            la función con fechas fijas.

    Retorna:
        bool: True si la fecha es válida y no es posterior a hoy.
    """
    recepcion = convertir_fecha(fecha_texto)
    if recepcion is None:
        return False

    hoy = hoy or date.today()
    return recepcion <= hoy


def validar_fecha_entrega(fecha_entrega: str, fecha_recepcion: str,
                          hoy: date | None = None) -> bool:
    """
    Valida la fecha en que se entregó la respuesta al poblador.

    Reglas de negocio:
        - La entrega no puede ser anterior a la recepción del documento.
        - La entrega no puede ser posterior a hoy (no se registra a futuro).

    Parámetros:
        fecha_entrega (str): fecha de entrega en formato dd/mm/aaaa.
        fecha_recepcion (str): fecha de recepción ya registrada del trámite.
        hoy (date | None): fecha de referencia; por defecto, la del sistema.

    Retorna:
        bool: True si la fecha de entrega cumple ambas reglas.
    """
    entrega = convertir_fecha(fecha_entrega)
    recepcion = convertir_fecha(fecha_recepcion)
    if entrega is None or recepcion is None:
        return False

    hoy = hoy or date.today()
    return recepcion <= entrega <= hoy


def validar_dni(dni: str) -> bool:
    """
    Verifica que el DNI tenga exactamente 8 dígitos numéricos.

    Parámetros:
        dni (str): DNI escrito por el usuario.

    Retorna:
        bool: True si el DNI tiene 8 caracteres y todos son dígitos.

    Ejemplo:
        >>> validar_dni("12345678")
        True
        >>> validar_dni("1234567A")
        False
    """
    return len(dni) == LONGITUD_DNI and dni.isdigit()


def validar_texto(texto: str) -> bool:
    """
    Verifica un campo de texto obligatorio (nombre, tipo de trámite o asunto).

    Además de exigir que no esté vacío, impide el carácter "|", porque es el
    separador del archivo de datos: si se permitiera, la línea quedaría con
    más de 8 campos y el trámite se perdería al volver a cargar el archivo.

    Parámetros:
        texto (str): valor ingresado por el usuario (ya sin espacios extremos).

    Retorna:
        bool: True si el texto no está vacío, no contiene "|" y no supera
        LONGITUD_MAXIMA_TEXTO caracteres.
    """
    return (texto != ""
            and SEPARADOR not in texto
            and len(texto) <= LONGITUD_MAXIMA_TEXTO)
