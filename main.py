"""
Sistema de Registro y Seguimiento de Trámites
Municipalidad del Centro Poblado de Samne (Otuzco, La Libertad - Perú)

Punto de entrada del programa: muestra el menú en consola y se comunica con
la secretaria (leer datos con input y mostrar resultados con print).

Las reglas de negocio están en tramites.py, las validaciones en
validaciones.py y el guardado en almacenamiento.py.

Uso:
    python main.py
"""

import almacenamiento
import tramites as reglas
from tramites import (CODIGO, FECHA_RECEPCION, DNI, NOMBRE, TIPO, ASUNTO,
                      ESTADO, FECHA_ENTREGA)
from validaciones import (validar_dni, validar_fecha_entrega,
                          validar_fecha_recepcion, validar_texto)

OPCION_SALIR = "6"


# ---------------------------------------------------------------------------
# Funciones auxiliares de entrada
# ---------------------------------------------------------------------------

def pedir_dato(mensaje: str, es_valido, mensaje_error: str) -> str:
    """
    Pide un dato al usuario hasta que cumpla la validación indicada.

    Centraliza el patrón "pedir - validar - volver a pedir" que antes se
    repetía en cada campo (principio DRY).

    Parámetros:
        mensaje (str): texto que se muestra al pedir el dato.
        es_valido (callable): función que recibe el texto y devuelve bool.
        mensaje_error (str): aviso que se muestra si el dato no es válido.

    Retorna:
        str: el dato ingresado, ya validado y sin espacios en los extremos.
    """
    dato = input(mensaje).strip()
    while not es_valido(dato):
        print(mensaje_error)
        dato = input(mensaje).strip()
    return dato


def pedir_texto_obligatorio(mensaje: str) -> str:
    """Pide un texto obligatorio (nombre, tipo o asunto) hasta que sea válido."""
    return pedir_dato(mensaje, validar_texto,
                      "Campo obligatorio. No puede estar vacío ni contener '|'.")


def mostrar_detalle(tramite: list[str]) -> None:
    """Muestra en pantalla los datos de un trámite del historial."""
    print("------------------------------")
    print("Código:", tramite[CODIGO])
    print("Fecha de ingreso:", tramite[FECHA_RECEPCION])
    print("Tipo:", tramite[TIPO])
    print("Asunto:", tramite[ASUNTO])
    print("Estado:", tramite[ESTADO])
    print("Fecha de entrega:", tramite[FECHA_ENTREGA])


# ---------------------------------------------------------------------------
# Opciones del menú
# ---------------------------------------------------------------------------

def registrar_tramite(lista: list[list[str]]) -> None:
    """Opción 1: pide y valida los datos, crea el trámite y lo guarda."""
    print("\n--- REGISTRAR TRÁMITE ---")
    fecha = pedir_dato("Fecha de recepción (dd/mm/aaaa): ",
                       validar_fecha_recepcion,
                       "Fecha incorrecta. No se permiten fechas futuras ni inválidas.")
    dni = pedir_dato("DNI: ", validar_dni, "El DNI debe tener 8 dígitos.")
    nombre = pedir_texto_obligatorio("Nombre del solicitante: ")
    tipo = pedir_texto_obligatorio("Tipo de trámite: ")
    asunto = pedir_texto_obligatorio("Asunto: ")

    nuevo = reglas.crear_tramite(lista, fecha, dni, nombre, tipo, asunto)
    almacenamiento.guardar_datos(lista)  # se guarda de inmediato: si se va la luz, no se pierde

    print("Trámite registrado correctamente.")
    print("Código:", nuevo[CODIGO])


def consultar_por_dni(lista: list[list[str]]) -> None:
    """Opción 2: muestra el historial de trámites de un ciudadano."""
    print("\n--- CONSULTA POR DNI ---")
    dni = input("Ingrese DNI: ").strip()
    encontrados = reglas.buscar_por_dni(lista, dni)

    if not encontrados:
        print("No existen trámites registrados para ese DNI.")
        return

    print("\nSolicitante:", encontrados[0][NOMBRE])
    print("HISTORIAL DE TRÁMITES")
    for tramite in encontrados:
        mostrar_detalle(tramite)


def mostrar_tramites(lista: list[list[str]]) -> None:
    """Opción 3: lista todos los trámites en una línea cada uno."""
    print("\n--- TODOS LOS TRÁMITES ---")
    if not lista:
        print("No existen registros.")
        return

    for t in lista:
        print(t[CODIGO], "-", t[DNI], "-", t[NOMBRE], "-", t[TIPO], "-", t[ESTADO])


def actualizar_estado(lista: list[list[str]]) -> None:
    """Opción 4: marca un trámite como ENTREGADO con su fecha de entrega."""
    print("\n--- ACTUALIZAR ESTADO ---")
    codigo = input("Código del trámite: ").strip().upper()
    tramite = reglas.buscar_por_codigo(lista, codigo)

    if tramite is None:
        print("Código no encontrado.")
        return

    print("Estado actual:", tramite[ESTADO])
    if tramite[ESTADO] == reglas.ESTADO_ENTREGADO:
        print("El trámite ya figura como entregado.")
        return

    fecha = pedir_dato(
        "Fecha de entrega (dd/mm/aaaa): ",
        lambda texto: validar_fecha_entrega(texto, tramite[FECHA_RECEPCION]),
        "Fecha incorrecta. La entrega no puede ser anterior a la recepción "
        "ni posterior a hoy.")

    reglas.marcar_entregado(tramite, fecha)
    almacenamiento.guardar_datos(lista)
    print("Estado actualizado correctamente.")


def ordenar_tramites(lista: list[list[str]]) -> None:
    """Opción 5: ordena por DNI (método burbuja) y muestra el resultado."""
    reglas.ordenar_por_dni(lista)
    print("Registros ordenados por DNI.")
    mostrar_tramites(lista)


# ---------------------------------------------------------------------------
# Menú principal
# ---------------------------------------------------------------------------

OPCIONES = {
    "1": registrar_tramite,
    "2": consultar_por_dni,
    "3": mostrar_tramites,
    "4": actualizar_estado,
    "5": ordenar_tramites,
}


def mostrar_menu() -> None:
    """Imprime las opciones del menú principal."""
    print("\nMUNICIPALIDAD DEL CENTRO POBLADO DE SAMNE")
    print("1. Registrar trámite")
    print("2. Buscar trámites por DNI")
    print("3. Mostrar todos los trámites")
    print("4. Actualizar estado")
    print("5. Ordenar registros")
    print("6. Salir")


def menu() -> None:
    """
    Controla la ejecución del programa.

    Carga los trámites al iniciar, repite el menú hasta que se elija "6" y
    guarda los datos antes de salir. Si ocurre un error inesperado, guarda lo
    registrado y muestra un mensaje simple, sin detalles técnicos.
    """
    lista = almacenamiento.cargar_datos()
    opcion = ""

    try:
        while opcion != OPCION_SALIR:
            mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()

            if opcion in OPCIONES:
                OPCIONES[opcion](lista)
            elif opcion != OPCION_SALIR:
                print("Opción no válida.")
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma interrumpido por el usuario.")
    except OSError:
        print("\nNo se pudo acceder al archivo de datos. Verifique la carpeta del programa.")
    finally:
        try:
            almacenamiento.guardar_datos(lista)
            print("Datos guardados. Fin del programa.")
        except OSError:
            print("No se pudieron guardar los datos. Avise al encargado del sistema.")


# Solo se ejecuta el menú cuando se corre "python main.py".
# Así las pruebas pueden importar este archivo sin abrir el menú.
if __name__ == "__main__":
    menu()
