# Sistema de Registro y Seguimiento de Trámites Municipales – Samne

Prototipo académico en Python para registrar, consultar, ordenar y dar seguimiento
a los trámites de la **Municipalidad del Centro Poblado de Samne** (Otuzco, La Libertad),
que hoy se llevan a mano en cuadernos de cargo. Funciona en consola y **sin Internet**.

## Requisitos

- Python **3.10 o superior** (solo usa la biblioteca estándar: no hay que instalar paquetes).

## Ejecución

```bash
python main.py
```

| Opción | Acción |
|-------|--------|
| 1 | Registrar trámite (fecha, DNI, nombre, tipo, asunto). Genera el código `TRA-0001`, `TRA-0002`… |
| 2 | Buscar el historial de trámites de un ciudadano por DNI |
| 3 | Mostrar todos los trámites |
| 4 | Marcar un trámite como ENTREGADO con su fecha de entrega |
| 5 | Ordenar los registros por DNI (método burbuja) |
| 6 | Guardar y salir |

Los datos se guardan en `tramites_samne.txt` (se crea solo en la primera ejecución).

## Pruebas

```bash
python -m unittest discover -s tests -v
```

36 pruebas automáticas (casos normales, límite y de error). También se ejecutan solas
en GitHub Actions cada vez que se hace `push` o se abre un Pull Request.

## Estructura del proyecto

```
Proyecto_Samne-/
├── main.py              # Menú en consola: pide datos y muestra resultados
├── tramites.py          # Reglas de negocio: código, búsqueda, entrega, ordenamiento
├── validaciones.py      # Validación de fechas, DNI y textos
├── almacenamiento.py    # Lectura y escritura de tramites_samne.txt
├── tests/
│   ├── test_validaciones.py
│   └── test_tramites.py
├── docs/
│   └── decisiones.md    # Registro de decisiones técnicas
├── .github/
│   ├── workflows/pruebas.yml        # Pruebas automáticas
│   └── pull_request_template.md     # Lista de revisión de código
├── .gitignore           # Excluye tramites_samne.txt (datos personales)
└── README.md
```

## Formato del archivo de datos

Una línea por trámite, 8 campos separados por `|`:

```
codigo|fecha_recepcion|dni|nombre|tipo|asunto|estado|fecha_entrega
TRA-0001|01/10/2026|45678912|Diego Martinez|Permiso|Uso de local|PENDIENTE|-
```

## Validaciones

- **Fechas:** formato `dd/mm/aaaa` y fecha real (no acepta `31/09/2026`).
- **Recepción:** no puede ser posterior a hoy.
- **Entrega:** no puede ser anterior a la recepción ni posterior a hoy.
- **DNI:** exactamente 8 dígitos.
- **Nombre, tipo y asunto:** obligatorios, máximo 100 caracteres y sin el carácter `|`
  (es el separador del archivo; si se permitiera, el trámite se perdería al recargar).
- Un trámite ENTREGADO no puede volver a entregarse.

## Seguridad y datos personales

`tramites_samne.txt` contiene DNI y nombres de pobladores, por eso está en `.gitignore`
y **nunca** se sube a GitHub. Para hacer pruebas se usan datos ficticios.

## Flujo de trabajo con Git

```bash
git checkout -b feature/nombre-de-la-mejora   # una rama por cambio
# ... programar y ejecutar las pruebas ...
git commit -m "feat: descripción corta del cambio"
git push -u origin feature/nombre-de-la-mejora
# Abrir Pull Request hacia main; se fusiona cuando las pruebas pasan y un compañero lo aprueba
```

Prefijos de commit: `feat:` (nueva función), `fix:` (corrección), `docs:` (documentación),
`test:` (pruebas), `refactor:` (mejora sin cambiar el comportamiento).

## Alcances y limitaciones

Prototipo local con archivo de texto. Aún no incluye autenticación de usuarios, uso
simultáneo desde varias computadoras ni copias de seguridad automáticas.

## Contexto académico

- **Curso:** Fundamentos de Programación – Universidad Privada del Norte
- **Docente:** Anthony Hans Delgado Chavarría
- **Equipo:** Alegre Pereira, Jhoel Harold · Zavaleta Abanto, Piero Alessandro ·
  Castañeda Alcántara, Hummer Sthif · Tapia Fernández, Angel Daniel · Martínez Guevara, Diego
