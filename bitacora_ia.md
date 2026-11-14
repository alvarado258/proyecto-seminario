# Bitácora de uso de IA

**Proyecto:** Tienda local con pruebas automatizadas  
**Estudiante:** Juan David Alvarado Cuéllar  
**Funcionalidad:** HU02 — Calcular el total de una compra  
**Asistente utilizado:** ChatGPT (chat para propuesta de código, pruebas y revisión)

> Este registro describe decisiones adoptadas al elaborar esta entrega con asistencia de IA. No se atribuyen mensajes textuales ni decisiones no verificadas al estudiante. Las verificaciones están disponibles en `evidencias/` y el historial Git.

## Entradas

### Entrada 1
- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Diseñar pruebas del contrato `calcular_total(precio, cantidad, descuento)` antes de escribir su implementación, usando pytest.
- **Decisión:** Aceptada.
- **Por qué:** La actividad exige pruebas primero y el diseño de semana 4 define resultados y excepciones concretos.
- **Verificación:** La primera ejecución terminó en rojo por `NotImplementedError` y se registró en `evidencias/pruebas_rojo.txt`.
- **Commit relacionado:** `test: pruebas HU02 inicialmente en rojo`.

### Entrada 2
- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Probar también descuento 100 %, precio cero, redondeo y entradas inválidas, además de las compras habituales.
- **Decisión:** Aceptada.
- **Por qué:** Son casos límite y de error explícitos en HU01/HU02; previenen defectos al modificar descuentos o validaciones.
- **Verificación:** `python -m pytest -q` en la etapa verde cubre casos normales, límites y excepciones.
- **Commit relacionado:** `test: pruebas HU02 inicialmente en rojo`.

### Entrada 3
- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Implementar el cálculo monetario con `Decimal` y redondeo `ROUND_HALF_UP` al final, en lugar de usar operaciones `float`.
- **Decisión:** Aceptada con cambios.
- **Por qué:** Se mantuvo la firma de la semana 4 y se agregaron validaciones previas de tipo y rango para cumplir HU01.
- **Verificación:** Pasan las pruebas, incluyendo `0.05 × 0.90 → 0.05` y las entradas inválidas.
- **Commit relacionado:** `feat: implementar calculo de total y pasar pruebas`.

### Entrada 4
- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Separar toda la validación de `calcular_total` para que la función solo calcule y redondee.
- **Decisión:** Aceptada.
- **Por qué:** Coincide con las dos operaciones propuestas en la interfaz de semana 4 y reduce responsabilidades en HU02.
- **Verificación:** Tras crear `validar_entrada`, la misma suite se mantuvo en verde sin editar `test_tienda.py`.
- **Commit relacionado:** `refactor: extraer validacion de entradas sin cambiar pruebas`.

### Entrada 5
- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Ampliar esta primera funcionalidad con servidor web, base de datos y autenticación.
- **Decisión:** Rechazada.
- **Por qué:** La alternativa B y el ADR-001 de semana 4 establecen una aplicación local modular; la rúbrica pide una función pequeña, no una aplicación completa.
- **Verificación:** El repositorio ejecuta el cálculo sin servicios externos y solo declara `pytest` como dependencia de pruebas.
- **Commit relacionado:** `refactor: extraer validacion de entradas sin cambiar pruebas`.

## Resumen

| Decisión | Cantidad |
|---|---:|
| Aceptadas | 3 |
| Aceptadas con cambios | 1 |
| Rechazadas | 1 |

## Errores que atraparon las pruebas

En la etapa inicial, la prueba de descuento del 100 % y el resto de casos fallaron porque `calcular_total` todavía generaba `NotImplementedError`. Esto confirmó que las pruebas se escribieron antes de implementar. Luego, los casos de descuento completo, precio negativo y redondeo comprobaron que la implementación conserva los comportamientos esperados. **No se afirma que apareciera un fallo adicional del código generado: no ocurrió durante las ejecuciones registradas.**

## Reflexión final

La IA ayudó a organizar las pruebas y a convertir el contrato del diseño en código ejecutable.  
Lo más útil fue identificar límites como el 100 % de descuento y los precios negativos.  
Las pruebas en rojo mostraron que el comportamiento todavía no estaba implementado.  
La implementación posterior pasó los casos previstos sin cambiar las pruebas.  
Separar la validación del cálculo hizo que el código resultara más fácil de explicar.  
Rechacé añadir un servidor porque no hacía falta para esta primera entrega.  
En la siguiente funcionalidad prepararía primero más casos de integración y los informes JSON.

## Semana 6 — 14 de noviembre de 2026

### 1. Revisión del código con IA
Usé ChatGPT para revisar la validación y el cálculo. Reproduje el fallo
con precio `1e28`, cantidad `1` y descuento `0`. La versión original
lanzaba `decimal.InvalidOperation` al redondear.

### 2. Corrección y prueba de regresión
Con apoyo de ChatGPT convertí el fallo decimal en un `ValueError`
que la consola puede mostrar. Agregué una prueba para `1e28` y
verifiqué que pasaron las 19 pruebas. Commit `62c0836`.

### 3. Configuración de Ruff y auditoría
Consulté a ChatGPT por los siete avisos S101. Revisé que los `assert`
estaban en las pruebas y limité la excepción a `test_tienda.py`.
Ruff pasó y `pip-audit` no encontró vulnerabilidades conocidas en
las dependencias revisadas. Commit `316145c`.