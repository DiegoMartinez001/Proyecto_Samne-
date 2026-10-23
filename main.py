ARCHIVO = "tramites_samne.txt"
tramites = []
 
def cargar_datos():
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
    archivo = open(ARCHIVO, "w", encoding="utf-8")
    for t in tramites:
        archivo.write("|".join(t) + "\n")
    archivo.close()
 
def generar_codigo():
    mayor = 0
    for t in tramites:
        numero = int(t[0][4:])
        if numero > mayor:
            mayor = numero
    return "TRA-" + str(mayor + 1).zfill(4)
 
def registrar_tramite():
    print("\n--- REGISTRAR TRÁMITE ---")
    fecha = input("Fecha de recepción (dd/mm/aaaa): ").strip()
 
    dni = input("DNI: ").strip()
    while len(dni) != 8 or not dni.isdigit():
        print("El DNI debe tener 8 dígitos.")
        dni = input("DNI: ").strip()
 
    nombre = input("Nombre del solicitante: ").strip()
    tipo = input("Tipo de trámite: ").strip()
    asunto = input("Asunto: ").strip()
 
    if fecha == "" or nombre == "" or tipo == "" or asunto == "":
        print("No se puede registrar. Existen campos obligatorios vacíos.")
        return
 
    codigo = generar_codigo()
    estado = "PENDIENTE"
    fecha_entrega = "-"
 
    nuevo = [codigo, fecha, dni, nombre, tipo, asunto, estado, fecha_entrega]
    tramites.append(nuevo)
    guardar_datos()
 
    print("Trámite registrado correctamente.")
    print("Código:", codigo)
 
def buscar_por_dni():
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
    print("\n--- TODOS LOS TRÁMITES ---")
    if len(tramites) == 0:
        print("No existen registros.")
        return
 
    for t in tramites:
        print(t[0], "-", t[2], "-", t[3], "-", t[4], "-", t[6])
 
def actualizar_estado():
    print("\n--- ACTUALIZAR ESTADO ---")
    codigo = input("Código del trámite: ").strip().upper()
 
    for t in tramites:
        if t[0] == codigo:
            print("Estado actual:", t[6])
 
            if t[6] == "ENTREGADO":
                print("El trámite ya figura como entregado.")
                return
 
            fecha = input("Fecha de entrega (dd/mm/aaaa): ").strip()
            if fecha == "":
                print("Debe ingresar la fecha de entrega.")
                return
 
            t[6] = "ENTREGADO"
            t[7] = fecha
            guardar_datos()
            print("Estado actualizado correctamente.")
            return
 
    print("Código no encontrado.")
 
def ordenar_tramites():
    n = len(tramites)
 
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if tramites[j][2] > tramites[j + 1][2]:
                auxiliar = tramites[j]
                tramites[j] = tramites[j + 1]
                tramites[j + 1] = auxiliar
 
    print("Registros ordenados por DNI.")
    mostrar_tramites()
 
def menu():
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