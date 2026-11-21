# Registro de decisiones técnicas – Proyecto Samne

Cada decisión indica la fecha, qué se decidió y por qué.

| Fecha | Decisión | Motivo |
|-------|----------|--------|
| 22/10/2026 | Programa local en consola (Python) en lugar de sistema web | La municipalidad no tiene Internet permanente (entrevista del 25/09/2026). |
| 22/10/2026 | Guardar en archivo de texto `tramites_samne.txt` separado por `\|` | Sin instalar nada adicional; se puede abrir con el Bloc de notas si falla el programa. |
| 22/10/2026 | Búsqueda principal por DNI | Es lo que la secretaria pidió: ver todo lo que pidió un poblador y cómo va. |
| 22/10/2026 | Código correlativo `TRA-0001` basado en el número mayor | Si se borra una línea, no se repiten códigos. |
| 23/10/2026 | La fecha de entrega no puede ser anterior a la recepción ni posterior a hoy | Evita registros imposibles en el historial. |
| 12/11/2026 | Separar el código en `main.py`, `tramites.py`, `validaciones.py` y `almacenamiento.py` | Cada archivo tiene una sola responsabilidad y la lógica se puede probar sin el menú. |
| 12/11/2026 | Prohibir el carácter `\|` en nombre, tipo y asunto | Se comprobó que un asunto con `\|` hacía que el trámite se borrara del archivo al reiniciar. |
| 12/11/2026 | Mantener el método burbuja (con salida anticipada) | Es requisito del curso (RF06). Medido: 1 000 trámites se ordenan en ~0,03 s, suficiente para el volumen de Samne. |
| 12/11/2026 | Pruebas con `unittest` | Viene incluido en Python: no hay que instalar nada en la computadora de la municipalidad. |
| 21/11/2026 | Reutilizar el nombre ya registrado cuando el DNI tiene trámites | En el archivo real el DNI 47250619 figuraba con dos nombres distintos, lo que partía el historial de una misma persona. |
