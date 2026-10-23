# Sistema de Registro y Seguimiento de Trámites Municipales

## 1. Descripción del proyecto

El presente proyecto consiste en el desarrollo de un prototipo de sistema de registro y seguimiento de trámites para la Municipalidad del Centro Poblado de Samne.

La propuesta surge ante la necesidad de mejorar el proceso de registro, búsqueda y seguimiento de solicitudes municipales, que actualmente se realiza de manera manual mediante cuadernos físicos.

El sistema está desarrollado en Python y funciona mediante un menú interactivo en la consola, sin necesidad de conexión a Internet.

## 2. Objetivo

Desarrollar un prototipo informático que permita registrar, consultar, organizar y actualizar el estado de los trámites municipales, facilitando la gestión de información y reduciendo la dependencia de los registros manuales.

## 3. Funcionalidades del sistema

El programa cuenta con seis opciones principales:

1. **Registrar trámite:** permite ingresar la fecha de recepción, DNI, nombre del solicitante, tipo de trámite y asunto. Genera automáticamente un código único.
2. **Buscar trámites por DNI:** permite consultar el historial de solicitudes de un ciudadano.
3. **Mostrar todos los trámites:** presenta los registros almacenados en el sistema.
4. **Actualizar estado:** permite cambiar un trámite de PENDIENTE a ENTREGADO, registrando su fecha de entrega.
5. **Ordenar registros:** organiza los trámites según el DNI del solicitante.
6. **Salir:** guarda la información y finaliza la ejecución del programa.

## 4. Herramientas utilizadas

- Lenguaje de programación: Python.
- Entorno de desarrollo: Visual Studio Code.
- Control de versiones: Git.
- Repositorio de código: GitHub.
- Almacenamiento de datos: archivo de texto local.

## 5. Conceptos de programación aplicados

El proyecto utiliza conceptos fundamentales de programación:

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

- `main.py`: contiene el código principal del sistema.
- `tramites_samne.txt`: almacena los registros de trámites.
- `.gitignore`: excluye determinados archivos del control de versiones.
- `README.md`: contiene la documentación del proyecto.

## 7. Ejecución del programa

Para ejecutar el sistema:

1. Instalar Python en la computadora.
2. Abrir la carpeta del proyecto en Visual Studio Code.
3. Abrir una terminal.
4. Ejecutar el siguiente comando:

`python main.py`

5. Seleccionar una opción del menú principal.

Los registros se almacenan localmente en el archivo `tramites_samne.txt`.

## 8. Validaciones implementadas

El sistema incorpora las siguientes validaciones:

- Verificación del formato y validez de las fechas ingresadas.
- Verificación de que el DNI contenga exactamente ocho dígitos numéricos al registrar trámites.
- Comprobación de campos obligatorios durante el registro.
- Generación automática de códigos correlativos.
- Verificación de la existencia del código antes de actualizar un trámite.
- Restricción para evitar actualizar nuevamente un trámite entregado.

## 9. Alcances y limitaciones

El programa constituye un prototipo académico desarrollado para demostrar la aplicación de los fundamentos de programación en una situación real.

Funciona de manera local, sin conexión a Internet, y utiliza un archivo de texto como mecanismo de almacenamiento.

No contempla todavía autenticación de usuarios, acceso simultáneo desde varias computadoras ni copias de seguridad automáticas.

## 10. Control de versiones

Se utiliza Git para registrar los cambios realizados durante el desarrollo y GitHub para conservar el código fuente y su historial de versiones.

## 11. Contexto académico

Proyecto desarrollado para el curso de Fundamentos de Programación.

Caso de estudio: Municipalidad del Centro Poblado de Samne, Perú.