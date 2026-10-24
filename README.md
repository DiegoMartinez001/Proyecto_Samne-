# Sistema de Registro y Seguimiento de Trámites Municipales

## 1. Descripción del proyecto

El presente proyecto consiste en el desarrollo de un prototipo de sistema de registro y seguimiento de trámites para la Municipalidad del Centro Poblado de Samne.

La propuesta surge ante la necesidad de mejorar el proceso de registro, búsqueda y seguimiento de solicitudes municipales, que actualmente se realiza de manera manual mediante cuadernos físicos.

El sistema está desarrollado en Python y funciona mediante un menú interactivo en la consola, sin necesidad de conexión a Internet.

## 2. Objetivo

Desarrollar un prototipo informático que permita registrar, consultar, organizar y actualizar el estado de los trámites municipales, facilitando la gestión de información y reduciendo la dependencia de los registros manuales.

## 3. Funcionalidades del sistema

El programa cuenta con seis opciones principales:

1. **Registrar trámite:** permite ingresar la fecha de recepción, DNI, nombre del solicitante, tipo de trámite y asunto. Genera automáticamente un código correlativo.
2. **Buscar trámites por DNI:** permite consultar el historial de solicitudes de un ciudadano.
3. **Mostrar todos los trámites:** presenta los registros almacenados en el sistema.
4. **Actualizar estado:** permite cambiar un trámite de PENDIENTE a ENTREGADO, registrando su fecha de entrega.
5. **Ordenar registros:** organiza los trámites según el DNI del solicitante mediante el algoritmo de ordenamiento de burbuja.
6. **Salir:** guarda la información y finaliza la ejecución del programa.

## 4. Herramientas utilizadas

- **Lenguaje de programación:** Python.
- **Entorno de desarrollo:** Visual Studio Code.
- **Control de versiones:** Git.
- **Repositorio de código:** GitHub.
- **Almacenamiento de datos:** archivo de texto local (TXT).

## 5. Conceptos de programación aplicados

El proyecto utiliza los siguientes conceptos fundamentales de programación:

- Variables y tipos de datos.
- Estructuras secuenciales.
- Estructuras condicionales (`if`, `elif`, `else`).
- Estructuras repetitivas (`for`, `while`).
- Funciones.
- Listas.
- Validación de datos.
- Lectura y escritura de archivos.
- Algoritmo de ordenamiento de burbuja.

## 6. Estructura del proyecto

El proyecto contiene los siguientes archivos:

- `main.py`: contiene el código principal del sistema.
- `tramites_samne.txt`: almacena localmente los registros de trámites.
- `.gitignore`: permite excluir determinados archivos del control de versiones.
- `README.md`: contiene la documentación del proyecto.

El archivo `tramites_samne.txt` se utiliza para almacenar los datos generados durante la ejecución del programa y no necesita publicarse en GitHub.

## 7. Ejecución del programa

Para ejecutar el sistema:

1. Instalar Python en la computadora.
2. Abrir la carpeta del proyecto en Visual Studio Code.
3. Abrir una terminal.
4. Ejecutar el siguiente comando:

```bash
python main.py
```

5. Seleccionar una opción del menú principal.

Los registros se almacenan localmente en el archivo `tramites_samne.txt`.

Si el archivo no existe, el programa permite comenzar con una lista vacía y lo crea al guardar los registros.

## 8. Validaciones implementadas

El sistema incorpora las siguientes validaciones:

**Validación de fechas:**
- Verifica que las fechas ingresadas sean válidas.
- No permite registrar fechas de recepción posteriores a la fecha actual.
- No permite registrar fechas de entrega anteriores a la fecha de recepción.
- No permite registrar fechas de entrega posteriores a la fecha actual.

**Validación de datos del solicitante:**
- Verifica que el DNI contenga exactamente ocho dígitos numéricos.
- Comprueba que los campos de nombre, tipo de trámite y asunto no estén vacíos.

**Validación de trámites:**
- Genera automáticamente códigos correlativos.
- Comprueba la existencia del código antes de actualizar un trámite.
- Impide actualizar nuevamente un trámite que ya figura como ENTREGADO.
- Guarda los cambios realizados en el archivo de texto.

## 9. Alcances y limitaciones

El programa constituye un prototipo académico desarrollado para demostrar la aplicación de los fundamentos de programación en una situación real.

Funciona de manera local, sin conexión a Internet, y utiliza un archivo de texto como mecanismo de almacenamiento.

El sistema permite realizar operaciones básicas de registro, consulta, actualización y organización de trámites municipales.

No contempla todavía autenticación de usuarios, acceso simultáneo desde varias computadoras ni copias de seguridad automáticas.

## 10. Control de versiones

Se utiliza Git para registrar los cambios realizados durante el desarrollo y GitHub para conservar el código fuente y su historial de versiones.

Durante el desarrollo se registraron las siguientes mejoras:

1. Creación de la versión inicial del prototipo.
2. Incorporación de validaciones de fecha y DNI.
3. Elaboración de la documentación del proyecto.
4. Implementación de restricciones adicionales para las fechas de recepción y entrega.

**Repositorio:** DiegoMartinez001/Proyecto_Samne-

## 11. Contexto académico

**Curso:** Fundamentos de Programación.

**Caso de estudio:** Municipalidad del Centro Poblado de Samne, Perú.

**Tipo de proyecto:** Prototipo académico de sistema de registro y seguimiento de trámites municipales.

**Lenguaje de programación:** Python.