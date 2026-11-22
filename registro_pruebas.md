# Registro de pruebas — Semana 7

**Proyecto** Tienda local en Python  
**Estudiante** Juan David Alvarado Cuéllar

## 1. Tabla de casos

### `calcular_total`

**Regla.** El total se obtiene multiplicando el precio por la cantidad, aplicando el descuento y redondeando a dos decimales. Los descuentos entre 0 % y 100 %, incluidos ambos extremos, son válidos. Un descuento fuera de ese rango genera `ValueError`.

| Caso | Técnica | Entrada `(precio, cantidad, descuento)` | Resultado esperado | Justificación |
|---|---|---|---|---|
| CT-01 | Partición válida | `("1000.00", 2, "10")` | `Decimal("1800.00")` | Al subtotal de 2000 se le restan 200 de descuento. |
| CT-02 | Justo por debajo del máximo | `("1000.00", 2, "99.99")` | `Decimal("0.20")` | Se paga el 0.01 % de 2000. |
| CT-03 | Límite máximo válido | `("1000.00", 2, "100")` | `Decimal("0.00")` | El descuento cubre todo el subtotal. |
| CT-04 | Justo por encima del máximo | `("1000.00", 2, "100.01")` | `ValueError` | El descuento supera el máximo permitido. |
| CT-05 | Límite mínimo válido | `("1000.00", 2, "0")` | `Decimal("2000.00")` | Sin descuento se cobra el subtotal completo. |
| CT-06 | Justo por debajo del mínimo | `("1000.00", 2, "-0.01")` | `ValueError` | El descuento es menor que 0 %. |

CT-01, CT-02, CT-03 y CT-05 se ejecutan con `test_total_segun_descuento`. CT-04 se ejecuta con `test_rechaza_descuento_superior_al_maximo`. CT-06 se ejecuta con `test_rechaza_descuento_negativo`.

### `validar_entrada`

**Regla evaluada.** La cantidad debe ser un entero mayor o igual a 1. Los booleanos se rechazan con `TypeError`. Una cantidad entera menor que 1 genera `ValueError`.

| Caso | Técnica | Entrada `(precio, cantidad, descuento)` | Resultado esperado | Justificación |
|---|---|---|---|---|
| VE-01 | Límite mínimo válido | `("1000.00", 1, "10")` | `datos["cantidad"] == 1` | Uno es la menor cantidad permitida. |
| VE-02 | Justo por debajo del mínimo | `("1000.00", 0, "10")` | `ValueError` | Cero es un entero fuera del rango permitido. |
| VE-03 | Partición de tipo inválido | `("1000.00", True, "10")` | `TypeError` | La regla excluye los booleanos como cantidad. |

VE-01 se ejecuta con `test_acepta_cantidad_minima`. VE-02 y VE-03 se ejecutan con `test_rechaza_cantidad_invalida`.

### `main`

**Regla evaluada.** Si la compra es válida, la consola muestra el total y devuelve el código `0`. Si la cantidad es inválida, muestra un mensaje sobre el problema y devuelve el código `1`.

| Caso | Técnica | Entrada | Resultado esperado | Prueba |
|---|---|---|---|---|
| CL-01 | Partición válida | Precio `1000.00`, cantidad `2`, descuento `10` | Imprime `1800.00` y devuelve `0`. | `test_main_muestra_total` |
| CL-02 | Límite inválido | Precio `1000.00`, cantidad `0`, descuento `10` | Informa el error de cantidad y devuelve `1`. | `test_main_informa_cantidad_invalida` |

### Tabla de decisión de `calcular_total`

La tabla usa un precio válido y distingue la validación de la cantidad de la aplicación del descuento.

| Cantidad | Descuento | Acción esperada | Cobertura |
|---|---|---|---|
| Booleana | Cualquiera | Lanzar `TypeError` durante la validación. | VE-03 prueba la validación directamente. |
| Entera menor que 1 | Cualquiera | Lanzar `ValueError` durante la validación. | VE-02 prueba la validación y CL-02 comprueba su efecto en consola. |
| Entera mayor o igual a 1 | Menor que 0 % | Lanzar `ValueError`. | CT-06 |
| Entera mayor o igual a 1 | Igual a 0 % | Devolver el subtotal redondeado. | CT-05 |
| Entera mayor o igual a 1 | Mayor que 0 % y menor que 100 % | Aplicar el descuento y redondear. | CT-01 y CT-02 |
| Entera mayor o igual a 1 | Igual a 100 % | Devolver `Decimal("0.00")`. | CT-03 |
| Entera mayor o igual a 1 | Mayor que 100 % | Lanzar `ValueError`. | CT-04 |

## 2. Revisión de las pruebas

| Hallazgo | Corrección | Motivo |
|---|---|---|
| En CT-01 se escribió `Decimal("1.000 × 2")`. | Se usó `Decimal("1800.00")`. | `Decimal` recibe un número escrito como texto. El resultado se obtuvo restando 200 al subtotal de 2000. |
| En CT-02 se esperaba `0.01` como total. | Se cambió el esperado a `Decimal("0.20")`. | El `0.01 %` es la proporción que queda por pagar. El valor en dinero es `2000 × 0.0001`. |
| El primer `assert` quedó fuera de su función y pytest reportó `NameError`. | Se corrigió la sangría del `assert`. | La variable `total` existe dentro de la función de prueba. |

**Ejecución final.** El comando `py -m pytest .\tests\test_semana7.py -v` reportó `11 passed`.

## 3. Errores introducidos a propósito

Los experimentos se realizaron de uno en uno, cuando la suite de Semana 7 tenía nueve casos. Se restauró el código original antes de agregar los dos casos del límite inferior del descuento.

| Cambio temporal en `tienda.py` | Pruebas que detectaron el error | Resultado observado |
|---|---|---|
| Cambiar el límite superior del descuento de `<=` a `<`. | `test_total_segun_descuento[100-0.00]` falló con `ValueError` porque el programa rechazó el 100 %. | 1 fallida y 8 aprobadas. |
| Cambiar `cantidad < 1` por `cantidad < 0`. | `test_rechaza_cantidad_invalida[0-ValueError]` falló porque no se lanzó la excepción. `test_main_informa_cantidad_invalida` falló porque la consola aceptó la compra e indicó éxito con el código `0`. | 2 fallidas y 7 aprobadas. |
| Fijar `factor_descuento = 1`. | Fallaron los tres casos de `test_total_segun_descuento` que existían en ese momento y `test_main_muestra_total`. El programa cobró `2000.00` sin aplicar el descuento. | 4 fallidas y 5 aprobadas. |

Después de los experimentos se dejaron los dos límites originales y se restauró la fórmula del descuento.

## 4. Datos de prueba

El fixture `compra_sintetica` proporciona una compra ficticia con precio unitario de `1000.00` y cantidad de `2`. Así se reutilizan los datos y se pueden comprobar los cálculos a mano. Los descuentos `-0.01`, `0`, `99.99`, `100` y `100.01` cubren los dos extremos del rango. Las cantidades `1`, `0` y `True` permiten distinguir el mínimo válido, un valor fuera del rango y un tipo rechazado.