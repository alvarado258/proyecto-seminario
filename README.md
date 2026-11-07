# Tienda local: cálculo de compras y pruebas automatizadas

**Estudiante:** Juan David Alvarado Cuéllar  
**Asignatura:** Seminario en Inteligencia Artificial Aplicada al Ciclo de Vida del Software  
**Entrega:** Semana 5 (7 de noviembre de 2026)

Este repositorio corresponde a la primera funcionalidad de la aplicación local modular en Python propuesta en el documento de diseño de semana 4 (alternativa B, ADR-001). El alcance implementado es **HU02**, apoyada en las reglas de entrada de **HU01**. El ejecutor de informes JSON (HU03–HU05) se mantiene como trabajo futuro, según el diseño.

## Funcionalidad de la semana 5

**HU02 — Calcular el total de una compra (Must).** Como encargado de la tienda, quiero conocer el total de una compra para cobrar el valor correcto después de aplicar un descuento.

**Criterios de aceptación:**
- Dado un precio no negativo, cantidad entera mayor o igual a 1 y descuento entre 0 y 100, cuando calculo el total, entonces obtengo `precio × cantidad × (1 − descuento / 100)` redondeado a dos decimales.
- Dado un descuento de 100 %, cuando calculo el total, entonces obtengo `0.00`.
- Dado un precio negativo, cantidad inválida, descuento fuera de rango o datos de tipo no permitido, cuando intento calcular, entonces recibo `ValueError` o `TypeError` según corresponda (HU01).

### Contrato

```python
calcular_total(precio: str, cantidad: int, descuento: str) -> Decimal
```

- **Entradas:** `precio` y `descuento` son cadenas con números decimales separados por punto; `cantidad` es un entero Python (no `bool`).
- **Salida:** un `Decimal` con dos decimales; no se guardan compras ni se modifica información externa.
- **Reglas:** precio ≥ 0; cantidad ≥ 1; descuento entre 0 y 100 inclusive. No se permiten NaN, infinito, textos no numéricos, cantidades fraccionarias o booleanas.
- **Redondeo:** `ROUND_HALF_UP`, aplicado una sola vez al total final, conforme a la decisión documentada en semana 4.
- **Errores:** `TypeError` para tipos no admitidos y `ValueError` para valor decimal no válido o fuera de rango.

| Precio | Cantidad | Descuento | Resultado esperado |
|---|---:|---|---|
| `"3333.00"` | 3 | `"10"` | `Decimal("8999.10")` |
| `"100.00"` | 1 | `"100"` | `Decimal("0.00")` |
| `"0.05"` | 1 | `"10"` | `Decimal("0.05")` |
| `"-10.00"` | 1 | `"0"` | `ValueError` |

### Instalación y ejecución

Con Python 3.11 o superior:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
python tienda.py --precio 3333.00 --cantidad 3 --descuento 10
```

Para una demostración sin instalar pytest, la última línea solo requiere Python. El programa muestra `8999.10`; ante entrada inválida informa el error y devuelve código de salida 1.

### Evidencia del ciclo pruebas primero

1. `test: pruebas HU02 inicialmente en rojo` — tests definidos; `calcular_total` pendiente de implementar.
2. `feat: implementar calculo de total y pasar pruebas` — primera versión funcional; suite en verde.
3. `refactor: extraer validacion de entradas sin cambiar pruebas` — introduce `validar_entrada`; mismas pruebas en verde.

Se puede revisar con `git log --oneline` y `git show <hash>`. **Los tests no se editaron entre los tres commits.** Las evidencias de terminal están en `evidencias/`.

### Límites de esta entrega

No se implementan aún informes JSON, runner ni interfaz gráfica. Esta primera entrega desarrolla una función principal, tal como exige semana 5. La HU02 se toma del diseño de semana 4; ese diseño indica expresamente que sus historias fueron supuestos académicos y no sustituye un documento original de semana 3.
