"""
Pruebas unitarias de tramites.py y pruebas de integración con
almacenamiento.py (guardar en un archivo y volver a cargar).

Ejecutar desde la carpeta del proyecto:
    python -m unittest discover -s tests -v
"""

import os
import tempfile
import unittest

import almacenamiento
from tramites import (DNI, ESTADO, FECHA_ENTREGA, NOMBRE, buscar_por_codigo,
                      buscar_por_dni, crear_tramite, generar_codigo,
                      marcar_entregado, nombre_registrado, ordenar_por_dni)


def tramite_de_prueba(codigo, dni, estado="PENDIENTE"):
    """Crea un trámite con datos ficticios para las pruebas."""
    return [codigo, "25/09/2026", dni, "Poblador de prueba", "Permiso",
            "Uso del local municipal", estado, "-"]


class PruebasCodigo(unittest.TestCase):

    def test_primer_codigo(self):                     # caso límite: lista vacía
        self.assertEqual(generar_codigo([]), "TRA-0001")

    def test_codigo_siguiente_al_mayor(self):         # caso normal
        lista = [tramite_de_prueba("TRA-0001", "11111111"),
                 tramite_de_prueba("TRA-0007", "22222222"),
                 tramite_de_prueba("TRA-0003", "33333333")]
        self.assertEqual(generar_codigo(lista), "TRA-0008")

    def test_codigo_danado_no_detiene_el_programa(self):   # caso de error
        lista = [tramite_de_prueba("TRA-00X1", "11111111"),
                 tramite_de_prueba("TRA-0002", "22222222")]
        self.assertEqual(generar_codigo(lista), "TRA-0003")


class PruebasRegistroYBusqueda(unittest.TestCase):

    def test_crear_tramite_queda_pendiente(self):     # caso normal
        lista = []
        nuevo = crear_tramite(lista, "25/09/2026", "45678912", "Diego Martinez",
                              "Permiso", "Uso de cancha")
        self.assertEqual(nuevo[0], "TRA-0001")
        self.assertEqual(nuevo[ESTADO], "PENDIENTE")
        self.assertEqual(len(lista), 1)

    def test_historial_con_varios_tramites(self):     # caso normal
        lista = [tramite_de_prueba("TRA-0001", "45678912"),
                 tramite_de_prueba("TRA-0002", "11111111"),
                 tramite_de_prueba("TRA-0003", "45678912")]
        self.assertEqual(len(buscar_por_dni(lista, "45678912")), 2)

    def test_dni_sin_tramites(self):                  # caso límite
        lista = [tramite_de_prueba("TRA-0001", "45678912")]
        self.assertEqual(buscar_por_dni(lista, "99999999"), [])

    def test_codigo_inexistente(self):                # caso de error
        self.assertIsNone(buscar_por_codigo([], "TRA-0099"))


class PruebasNombreRegistrado(unittest.TestCase):
    """Un mismo DNI debe conservar un solo nombre en el historial."""

    def test_dni_nuevo_no_tiene_nombre(self):         # caso límite
        lista = [tramite_de_prueba("TRA-0001", "45678912")]
        self.assertIsNone(nombre_registrado(lista, "11111111"))

    def test_dni_existente_devuelve_su_nombre(self):  # caso normal
        lista = []
        crear_tramite(lista, "01/10/2026", "47250619", "Diego Martinez Guevara",
                      "Carta", "Donacion de panes")
        self.assertEqual(nombre_registrado(lista, "47250619"),
                         "Diego Martinez Guevara")

    def test_nombres_distintos_toma_el_mas_antiguo(self):  # caso de error previo
        lista = [tramite_de_prueba("TRA-0009", "47250619"),
                 tramite_de_prueba("TRA-0006", "47250619")]
        lista[0][NOMBRE] = "DIEGO MARTINEZ GUEVARA"
        lista[1][NOMBRE] = "Deigo Martinwz Guevara"
        self.assertEqual(nombre_registrado(lista, "47250619"),
                         "Deigo Martinwz Guevara")


class PruebasActualizarEstado(unittest.TestCase):

    def test_marcar_entregado(self):                  # caso normal
        tramite = tramite_de_prueba("TRA-0001", "45678912")
        marcar_entregado(tramite, "28/09/2026")
        self.assertEqual(tramite[ESTADO], "ENTREGADO")
        self.assertEqual(tramite[FECHA_ENTREGA], "28/09/2026")

    def test_no_se_entrega_dos_veces(self):           # caso de error
        tramite = tramite_de_prueba("TRA-0001", "45678912", "ENTREGADO")
        with self.assertRaises(ValueError):
            marcar_entregado(tramite, "30/09/2026")


class PruebasOrdenamiento(unittest.TestCase):

    def test_ordena_por_dni(self):                    # caso normal
        lista = [tramite_de_prueba("TRA-0001", "70000000"),
                 tramite_de_prueba("TRA-0002", "10000000"),
                 tramite_de_prueba("TRA-0003", "40000000")]
        ordenar_por_dni(lista)
        self.assertEqual([t[DNI] for t in lista],
                         ["10000000", "40000000", "70000000"])

    def test_lista_vacia_y_de_un_elemento(self):      # caso límite
        vacia = []
        ordenar_por_dni(vacia)
        self.assertEqual(vacia, [])
        uno = [tramite_de_prueba("TRA-0001", "70000000")]
        ordenar_por_dni(uno)
        self.assertEqual(len(uno), 1)

    def test_resultado_igual_a_sorted(self):          # comparación con Python
        dnis = ["45678912", "00012345", "99999999", "45678912", "12345678"]
        lista = [tramite_de_prueba(f"TRA-{i:04d}", d) for i, d in enumerate(dnis)]
        ordenar_por_dni(lista)
        self.assertEqual([t[DNI] for t in lista], sorted(dnis))


class PruebasIntegracionArchivo(unittest.TestCase):
    """Guardar en un archivo temporal y volver a cargar (persistencia)."""

    def setUp(self):
        carpeta = tempfile.mkdtemp()
        self.ruta = os.path.join(carpeta, "tramites_prueba.txt")

    def test_guardar_y_cargar(self):                  # caso normal
        lista = [tramite_de_prueba("TRA-0001", "45678912"),
                 tramite_de_prueba("TRA-0002", "11111111")]
        almacenamiento.guardar_datos(lista, self.ruta)
        self.assertEqual(almacenamiento.cargar_datos(self.ruta), lista)

    def test_archivo_inexistente(self):               # caso límite
        self.assertEqual(almacenamiento.cargar_datos(self.ruta), [])

    def test_linea_danada_se_ignora(self):            # caso de error
        with open(self.ruta, "w", encoding="utf-8") as archivo:
            archivo.write("TRA-0001|25/09/2026|45678912|Ana|Permiso|Local|PENDIENTE|-\n")
            archivo.write("linea dañada sin separadores\n")
        self.assertEqual(len(almacenamiento.cargar_datos(self.ruta)), 1)


if __name__ == "__main__":
    unittest.main()
