"""Cálculo de compras de una tienda local (HU01/HU02)."""
import argparse
from decimal import Decimal, DecimalException, InvalidOperation, ROUND_HALF_UP

CENTAVO = Decimal("0.01")
PORCENTAJE_TOTAL = Decimal("100")


def validar_entrada(precio: str, cantidad: int, descuento: str) -> dict:
    """Valida y normaliza los tres datos de una compra (HU01)."""
    if not isinstance(precio, str) or not isinstance(descuento, str):
        raise TypeError("Precio y descuento deben ser textos decimales")
    if type(cantidad) is not int:  # bool es int en Python; aquí no se acepta.
        raise TypeError("Cantidad debe ser un entero")
    try:
        precio_decimal = Decimal(precio)
        descuento_decimal = Decimal(descuento)
    except InvalidOperation as error:
        raise ValueError("El precio o descuento no es decimal válido") from error
    if not precio_decimal.is_finite() or not descuento_decimal.is_finite():
        raise ValueError("No se permiten NaN ni infinito")
    if precio_decimal < 0:
        raise ValueError("El precio no puede ser negativo")
    if cantidad < 1:
        raise ValueError("La cantidad debe ser al menos 1")
    if not (0 <= descuento_decimal <= PORCENTAJE_TOTAL):
        raise ValueError("El descuento debe estar entre 0 y 100")
    return {"precio": precio_decimal, "cantidad": cantidad,
            "descuento": descuento_decimal}

    """Valida el precio, la cantidad y el descuento de una compra.

    Recibe precio y descuento como textos decimales y cantidad como entero.
    Devuelve un diccionario con el precio y el descuento como Decimal y la
    cantidad como int. Lanza TypeError por tipos incorrectos y ValueError
    por valores inválidos o fuera de rango.
    """

def calcular_total(precio: str, cantidad: int, descuento: str) -> Decimal:
    """Devuelve el total de la compra redondeado a dos decimales.

    Recibe el precio y el descuento como textos decimales y la cantidad
    como entero. Lanza TypeError si los tipos son incorrectos y ValueError
    si algún valor es inválido o el cálculo supera la precisión disponible.
    """
    datos = validar_entrada(precio, cantidad, descuento)
    try:
        subtotal = datos["precio"] * datos["cantidad"]
        factor_descuento = 1 - datos["descuento"] / PORCENTAJE_TOTAL
        total = subtotal * factor_descuento
        return total.quantize(CENTAVO, rounding=ROUND_HALF_UP)
    except DecimalException as error:
        raise ValueError("El total supera la precisión disponible") from error

def main() -> int:
    parser = argparse.ArgumentParser(description="Calcular total de compra")
    parser.add_argument("--precio", required=True)
    parser.add_argument("--cantidad", required=True, type=int)
    parser.add_argument("--descuento", required=True)
    args = parser.parse_args()
    try:
        print(calcular_total(args.precio, args.cantidad, args.descuento))
        return 0
    except (ValueError, TypeError) as error:
        print(f"Error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
