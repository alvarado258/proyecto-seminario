"""Cálculo de compras de una tienda local (HU01/HU02)."""
import argparse
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

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


def calcular_total(precio: str, cantidad: int, descuento: str) -> Decimal:
    """Obtiene el total descontado, redondeado una sola vez al final (HU02)."""
    datos = validar_entrada(precio, cantidad, descuento)
    subtotal = datos["precio"] * datos["cantidad"]
    factor_descuento = 1 - datos["descuento"] / PORCENTAJE_TOTAL
    return (subtotal * factor_descuento).quantize(CENTAVO, rounding=ROUND_HALF_UP)


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
