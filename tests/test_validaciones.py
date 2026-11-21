"""
Pruebas unitarias de validaciones.py.

Se usa una fecha "hoy" fija (12/11/2026) para que las pruebas den el mismo
resultado sin importar el día en que se ejecuten.

Ejecutar desde la carpeta del proyecto:
    python -m unittest discover -s tests -v
"""

import unittest
from datetime import date

from validaciones import (validar_dni, validar_fecha, validar_fecha_entrega,
                          validar_fecha_recepcion, validar_texto)

HOY = date(2026, 11, 12)


class PruebasFecha(unittest.TestCase):

    def test_fecha_valida(self):                      # caso normal
        self.assertTrue(validar_fecha("30/04/2026"))

    def test_29_febrero_anio_bisiesto(self):          # caso límite
        self.assertTrue(validar_fecha("29/02/2028"))

    def test_29_febrero_anio_no_bisiesto(self):       # caso de error
        self.assertFalse(validar_fecha("29/02/2026"))

    def test_formato_incorrecto(self):                # caso de error
        self.assertFalse(validar_fecha("2026-04-30"))
        self.assertFalse(validar_fecha(""))
        self.assertFalse(validar_fecha("hola"))


class PruebasFechaRecepcion(unittest.TestCase):

    def test_fecha_pasada(self):                      # caso normal
        self.assertTrue(validar_fecha_recepcion("25/09/2026", HOY))

    def test_fecha_de_hoy(self):                      # caso límite
        self.assertTrue(validar_fecha_recepcion("12/11/2026", HOY))

    def test_fecha_de_manana(self):                   # caso límite (error)
        self.assertFalse(validar_fecha_recepcion("13/11/2026", HOY))

    def test_fecha_inexistente(self):                 # caso de error
        self.assertFalse(validar_fecha_recepcion("31/09/2026", HOY))


class PruebasFechaEntrega(unittest.TestCase):

    def test_entrega_posterior_a_recepcion(self):     # caso normal
        self.assertTrue(validar_fecha_entrega("28/09/2026", "25/09/2026", HOY))

    def test_entrega_mismo_dia(self):                 # caso límite
        self.assertTrue(validar_fecha_entrega("25/09/2026", "25/09/2026", HOY))

    def test_entrega_hoy(self):                       # caso límite
        self.assertTrue(validar_fecha_entrega("12/11/2026", "25/09/2026", HOY))

    def test_entrega_antes_de_recepcion(self):        # caso de error
        self.assertFalse(validar_fecha_entrega("24/09/2026", "25/09/2026", HOY))

    def test_entrega_futura(self):                    # caso de error
        self.assertFalse(validar_fecha_entrega("13/11/2026", "25/09/2026", HOY))


class PruebasDni(unittest.TestCase):

    def test_dni_correcto(self):                      # caso normal
        self.assertTrue(validar_dni("45678912"))

    def test_dni_con_ceros_al_inicio(self):           # caso límite
        self.assertTrue(validar_dni("00012345"))

    def test_dni_con_siete_y_nueve_digitos(self):     # caso límite (error)
        self.assertFalse(validar_dni("1234567"))
        self.assertFalse(validar_dni("123456789"))

    def test_dni_con_letras_o_vacio(self):            # caso de error
        self.assertFalse(validar_dni("1234567A"))
        self.assertFalse(validar_dni(""))


class PruebasTexto(unittest.TestCase):

    def test_texto_normal(self):                      # caso normal
        self.assertTrue(validar_texto("Permiso para uso de cancha"))

    def test_texto_vacio(self):                       # caso de error
        self.assertFalse(validar_texto(""))

    def test_texto_con_separador(self):               # caso de error (seguridad)
        self.assertFalse(validar_texto("Permiso | baile social"))

    def test_texto_largo(self):                       # caso límite
        self.assertTrue(validar_texto("a" * 100))
        self.assertFalse(validar_texto("a" * 101))


if __name__ == "__main__":
    unittest.main()
