"""
Sistema de Registro y Seguimiento de Trámites
Municipalidad del Centro Poblado de Samne (Otuzco, La Libertad - Perú)

Prototipo académico del curso Fundamentos de Programación (UPN, 2026).
Permite registrar trámites, buscarlos por DNI, actualizar su estado,
ordenarlos por DNI (método burbuja) y guardarlos en un archivo de texto
local, sin necesidad de Internet.

Formato del archivo tramites_samne.txt: una línea por trámite con 8 campos
separados por "|":

    codigo|fecha_recepcion|dni|nombre|tipo|asunto|estado|fecha_entrega

Posición de cada campo en la lista de un trámite (t):
    t[0] código          t[4] tipo de trámite
    t[1] fecha recepción t[5] asunto
    t[2] DNI             t[6] estado (PENDIENTE / ENTREGADO)
    t[3] nombre          t[7] fecha de entrega ("-" si está pendiente)

El archivo contiene datos personales (DNI y nombres), por eso está en
.gitignore y no se sube a GitHub.

Uso:
    python main.py
"""

ARCHIVO = "tramites_samne.txt"  # archivo local donde se guardan los trámites
tramites = []                   # lista de trámites; cada trámite es una lista de 8 textos
 
def cargar_datos():
    """
    Carga los trámites guardados en tramites_samne.txt a la lista tramites.

    Si el archivo todavía no existe (primera ejecución), el programa empieza
    con la lista vacía. Solo se cargan las líneas que tienen los 8 campos.
    """
    try:
        archivo = open(ARCHIVO, "r", encoding="utf-8")
        for linea in archivo:
            datos = linea.strip().split("|")
            if len(datos) == 8:
                tramites.append(datos)
        archivo.close()
    except FileNotFoundError:
        pass
 
def guardar_datos():
    """
    Guarda todos los trámites de la lista en tramites_samne.txt.

    Reemplaza el contenido anterior del archivo: cada trámite se escribe en
    una línea con sus 8 campos unidos por "|".
    """
    archivo = open(ARCHIVO, "w", encoding="utf-8")
    for t in tramites:
        archivo.write("|".join(t) + "\n")
    archivo.close()
 
def generar_codigo():
    """
    Genera el siguiente código correlativo (TRA-0001, TRA-0002, ...).

    Busca el número mayor ya usado en lugar de contar los registros, para que
    el código siga siendo único aunque se borre una línea del archivo.

    Retorna:
        str: nuevo código, por ejemplo "TRA-0008".
    """
    mayor = 0
    for t in tramites:
        numero = int(t[0][4:])
        if numero > mayor:
            mayor = numero
    return "TRA-" + str(mayor + 1).zfill(4)  # zfill(4): 1 -> "0001"
 

from datetime import datetime

def validar_fecha(fecha):
    """
    Verifica que el texto sea una fecha real con formato dd/mm/aaaa.

    Parámetros:
        fecha (str): fecha escrita por el usuario, por ejemplo "30/04/2026".

    Retorna:
        bool: True si la fecha existe; False si el formato es incorrecto o la
        fecha no existe (por ejemplo "31/09/2026").
    """
    try:
        datetime.strptime(fecha, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def validar_fecha_recepcion(fecha):
    """
    Valida la fecha en que la municipalidad recibió el documento.

    Regla: la fecha debe ser válida y no puede ser posterior a hoy.

    Parámetros:
        fecha (str): fecha de recepción en formato dd/mm/aaaa.

    Retorna:
        bool: True si cumple la regla; False en caso contrario.
    """
    if not validar_fecha(fecha):
        return False

    fecha_ingresada = datetime.strptime(fecha, "%d/%m/%Y").date()
    fecha_actual = datetime.now().date()

    if fecha_ingresada > fecha_actual:
        return False
    return True
def validar_fecha_entrega(fecha_entrega, fecha_recepcion):
    """
    Valida la fecha en que se entregó la respuesta al poblador.

    Reglas: la entrega no puede ser anterior a la recepción del documento
    ni posterior a hoy.

    Parámetros:
        fecha_entrega (str): fecha de entrega en formato dd/mm/aaaa.
        fecha_recepcion (str): fecha de recepción ya registrada del trámite.

    Retorna:
        bool: True si la fecha de entrega cumple ambas reglas.
    """
    if not validar_fecha(fecha_entrega):
        return False

    entrega = datetime.strptime(fecha_entrega, "%d/%m/%Y").date()
    recepcion = datetime.strptime(fecha_recepcion, "%d/%m/%Y").date()
    hoy = datetime.now().date()

    if entrega < recepcion or entrega > hoy:
        return False

    return True
def registrar_tramite():
    """
    Opción 1 del menú: registra un trámite nuevo.

    Pide y valida la fecha de recepción y el DNI (8 dígitos), luego el nombre,
    el tipo de trámite y el asunto (obligatorios). Genera el código, deja el
    trámite en estado PENDIENTE y lo guarda en el archivo.
    """
    print("\n--- REGISTRAR TRÁMITE ---")
    fecha = input("Fecha de recepción (dd/mm/aaaa): ").strip()

    while not validar_fecha_recepcion(fecha):
        print("Fecha incorrecta. No se permiten fechas futuras ni inválidas.")
        fecha = input("Fecha de recepción (dd/mm/aaaa): ").strip()

    dni = input("DNI: ").strip()
    while len(dni) != 8 or not dni.isdigit():
        print("El DNI debe tener 8 dígitos.")
        dni = input("DNI: ").strip()

    nombre = input("Nombre del solicitante: ").strip()
    tipo = input("Tipo de trámite: ").strip()
    asunto = input("Asunto: ").strip()

    if nombre == "" or tipo == "" or asunto == "":
        print("No se puede registrar. Existen campos obligatorios vacíos.")
        return

    codigo = generar_codigo()
    estado = "PENDIENTE"
    fecha_entrega = "-"

    nuevo = [codigo, fecha, dni, nombre, tipo, asunto, estado, fecha_entrega]
    tramites.append(nuevo)
    guardar_datos()  # se guarda al registrar, no solo al salir: si se va la luz, no se pierde

    print("Trámite registrado correctamente.")
    print("Código:", codigo)

 
def buscar_por_dni():
    """
    Opción 2 del menú: muestra el historial de trámites de un ciudadano.

    Recorre toda la lista (búsqueda secuencial), porque una misma persona
    puede tener varios trámites registrados.
    """
    print("\n--- CONSULTA POR DNI ---")
    dni = input("Ingrese DNI: ").strip()
    encontrado = False
 
    for t in tramites:
        if t[2] == dni:
            if encontrado == False:
                print("\nSolicitante:", t[3])
                print("HISTORIAL DE TRÁMITES")
            print("------------------------------")
            print("Código:", t[0])
            print("Fecha de ingreso:", t[1])
            print("Tipo:", t[4])
            print("Asunto:", t[5])
            print("Estado:", t[6])
            print("Fecha de entrega:", t[7])
            encontrado = True
 
    if encontrado == False:
        print("No existen trámites registrados para ese DNI.")
 
def mostrar_tramites():
    """Opción 3 del menú: lista todos los trámites, uno por línea."""
    print("\n--- TODOS LOS TRÁMITES ---")
    if len(tramites) == 0:
        print("No existen registros.")
        return
 
    for t in tramites:
        print(t[0], "-", t[2], "-", t[3], "-", t[4], "-", t[6])
 
def actualizar_estado():
    """
    Opción 4 del menú: cambia un trámite de PENDIENTE a ENTREGADO.

    Busca el trámite por su código, impide actualizar uno que ya fue
    entregado y pide una fecha de entrega válida antes de guardar.
    """
    print("\n--- ACTUALIZAR ESTADO ---")
    codigo = input("Código del trámite: ").strip().upper()
 
    for t in tramites:
        if t[0] == codigo:
            print("Estado actual:", t[6])
 
            if t[6] == "ENTREGADO":  # no se sobrescribe la fecha de entrega original
                print("El trámite ya figura como entregado.")
                return
 
           
            fecha = input("Fecha de entrega (dd/mm/aaaa): ").strip()

            while not validar_fecha_entrega(fecha, t[1]):
                print("Fecha incorrecta. La entrega no puede ser anterior a la recepción ni posterior a hoy.")
                fecha = input("Fecha de entrega (dd/mm/aaaa): ").strip()

 
            t[6] = "ENTREGADO"
            t[7] = fecha
            guardar_datos()
            print("Estado actualizado correctamente.")
            return
 
    print("Código no encontrado.")
 
def ordenar_tramites():
    """
    Opción 5 del menú: ordena los trámites de menor a mayor DNI.

    Usa el método de burbuja (requisito RF06): compara pares vecinos y los
    intercambia si están en desorden. Los DNI se comparan como texto, lo cual
    es correcto porque todos tienen 8 dígitos.
    """
    n = len(tramites)
 
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if tramites[j][2] > tramites[j + 1][2]:
                auxiliar = tramites[j]  # intercambio de los dos trámites
                tramites[j] = tramites[j + 1]
                tramites[j + 1] = auxiliar
 
    print("Registros ordenados por DNI.")
    mostrar_tramites()
 
def menu():
    """
    Controla la ejecución del programa.

    Carga los trámites al iniciar, muestra el menú hasta que se elija la
    opción 6 y guarda los datos antes de salir.
    """
    cargar_datos()
    opcion = ""
 
    while opcion != "6":
        print("\nMUNICIPALIDAD DEL CENTRO POBLADO DE SAMNE")
        print("1. Registrar trámite")
        print("2. Buscar trámites por DNI")
        print("3. Mostrar todos los trámites")
        print("4. Actualizar estado")
        print("5. Ordenar registros")
        print("6. Salir")
 
        opcion = input("Seleccione una opción: ").strip()
 
        if opcion == "1":
            registrar_tramite()
        elif opcion == "2":
            buscar_por_dni()
        elif opcion == "3":
            mostrar_tramites()
        elif opcion == "4":
            actualizar_estado()
        elif opcion == "5":
            ordenar_tramites()
        elif opcion == "6":
            guardar_datos()
            print("Datos guardados. Fin del programa.")
        else:
            print("Opción no válida.")
 
menu()