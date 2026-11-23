"""
Reglas de negocio de los trámites municipales de Samne.

Este módulo no lee del teclado ni imprime en pantalla: solo trabaja con la
lista de trámites. La interacción con la secretaria está en main.py.

Cada trámite es una lista de 8 textos. Para no usar "números mágicos"
(t[2], t[6]...) se definen constantes con la posición de cada campo.
"""

# Posición de cada campo dentro de un trámite
CODIGO = 0
FECHA_RECEPCION = 1
DNI = 2
NOMBRE = 3
TIPO = 4
ASUNTO = 5
ESTADO = 6
FECHA_ENTREGA = 7

PREFIJO_CODIGO = "TRA-"
DIGITOS_CODIGO = 4
ESTADO_PENDIENTE = "PENDIENTE"
ESTADO_ENTREGADO = "ENTREGADO"
SIN_FECHA = "-"


def generar_codigo(tramites: list[list[str]]) -> str:
    """
    Genera el siguiente código correlativo (TRA-0001, TRA-0002, ...).

    Se busca el número mayor ya usado en lugar de contar los registros, para
    que el código siga siendo único aunque se elimine una línea del archivo.

    Parámetros:
        tramites (list[list[str]]): trámites registrados.

    Retorna:
        str: nuevo código, por ejemplo "TRA-0008".

    Ejemplo:
        >>> generar_codigo([])
        'TRA-0001'
    """
    mayor = 0
    for tramite in tramites:
        numero_texto = tramite[CODIGO][len(PREFIJO_CODIGO):]
        if numero_texto.isdigit():          # ignora códigos dañados
            mayor = max(mayor, int(numero_texto))
    return PREFIJO_CODIGO + str(mayor + 1).zfill(DIGITOS_CODIGO)


def crear_tramite(tramites: list[list[str]], fecha_recepcion: str, dni: str,
                  nombre: str, tipo: str, asunto: str) -> list[str]:
    """
    Crea un trámite nuevo en estado PENDIENTE y lo agrega a la lista.

    Los datos deben llegar ya validados (ver validaciones.py).

    Parámetros:
        tramites (list[list[str]]): lista donde se agrega el trámite.
        fecha_recepcion (str): fecha en formato dd/mm/aaaa.
        dni (str): DNI del solicitante (8 dígitos).
        nombre (str): nombre completo del solicitante.
        tipo (str): tipo de trámite (permiso, solicitud, oficio...).
        asunto (str): descripción breve del pedido.

    Retorna:
        list[str]: el trámite creado, con su código ya asignado.
    """
    nuevo = [generar_codigo(tramites), fecha_recepcion, dni, nombre, tipo,
             asunto, ESTADO_PENDIENTE, SIN_FECHA]
    tramites.append(nuevo)
    return nuevo


def buscar_por_dni(tramites: list[list[str]], dni: str) -> list[list[str]]:
    """
    Devuelve todos los trámites presentados por un mismo ciudadano.

    Búsqueda secuencial: recorre la lista completa porque una persona puede
    tener varios trámites (historial).

    Parámetros:
        tramites (list[list[str]]): trámites registrados.
        dni (str): DNI a buscar.

    Retorna:
        list[list[str]]: trámites encontrados (lista vacía si no hay).
    """
    return [tramite for tramite in tramites if tramite[DNI] == dni]


def nombre_registrado(tramites: list[list[str]], dni: str) -> str | None:
    """
    Devuelve el nombre con el que ya está registrado un DNI.

    Evita que una misma persona quede con nombres distintos en el historial
    (por ejemplo "Deigo Martínwz Guevara" y "DIEGO MARTINEZ GUEVARA" con el
    mismo DNI). Si el DNI tiene varios trámites, se toma el nombre del más
    antiguo, es decir, el de código menor.

    Parámetros:
        tramites (list[list[str]]): trámites registrados.
        dni (str): DNI del solicitante.

    Retorna:
        str | None: el nombre registrado, o None si el DNI es nuevo.

    Ejemplo:
        >>> nombre_registrado([], "45678912") is None
        True
    """
    encontrados = buscar_por_dni(tramites, dni)
    if not encontrados:
        return None
    mas_antiguo = min(encontrados, key=lambda tramite: tramite[CODIGO])
    return mas_antiguo[NOMBRE]


def buscar_por_codigo(tramites: list[list[str]], codigo: str) -> list[str] | None:
    """
    Busca un trámite por su código.

    Parámetros:
        tramites (list[list[str]]): trámites registrados.
        codigo (str): código a buscar, p. ej. "TRA-0003".

    Retorna:
        list[str] | None: el trámite encontrado, o None si no existe.
    """
    for tramite in tramites:
        if tramite[CODIGO] == codigo:
            return tramite
    return None


def marcar_entregado(tramite: list[str], fecha_entrega: str) -> None:
    """
    Cambia el estado de un trámite de PENDIENTE a ENTREGADO.

    Parámetros:
        tramite (list[str]): trámite a actualizar.
        fecha_entrega (str): fecha de entrega ya validada (dd/mm/aaaa).

    Lanza:
        ValueError: si el trámite ya figuraba como ENTREGADO, para no
        sobrescribir la fecha de entrega original.
    """
    if tramite[ESTADO] == ESTADO_ENTREGADO:
        raise ValueError("El trámite ya figura como entregado.")
    tramite[ESTADO] = ESTADO_ENTREGADO
    tramite[FECHA_ENTREGA] = fecha_entrega


def ordenar_por_dni(tramites: list[list[str]]) -> None:
    """
    Ordena los trámites de menor a mayor DNI con el método de burbuja.

    Se usa burbuja porque es un requisito del curso (RF06). Se comparan los
    DNI como texto, lo cual es correcto porque todos tienen 8 dígitos.
    Mejora: si en una pasada no hubo intercambios, la lista ya está ordenada
    y se termina antes.

    La lista se modifica en el mismo lugar (no se crea una copia).

    Parámetros:
        tramites (list[list[str]]): trámites a ordenar.

    Retorna:
        None
    """
    n = len(tramites)
    for pasada in range(n - 1):
        hubo_intercambio = False
        for j in range(n - 1 - pasada):
            if tramites[j][DNI] > tramites[j + 1][DNI]:
                tramites[j], tramites[j + 1] = tramites[j + 1], tramites[j]
                hubo_intercambio = True
        if not hubo_intercambio:
            break
