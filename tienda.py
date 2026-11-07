"""Cálculo de compras de una tienda local (HU02)."""
import argparse
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


def calcular_total(precio: str, cantidad: int, descuento: str) -> Decimal:
    """Calcula el total con descuento y redondeo monetario."""
    if not isinstance(precio, str) or not isinstance(descuento, str):
        raise TypeError("Precio y descuento deben ser textos decimales")
    if type(cantidad) is not int:
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
    if not (0 <= descuento_decimal <= 100):
        raise ValueError("El descuento debe estar entre 0 y 100")
    total = precio_decimal * cantidad * (1 - descuento_decimal / 100)
    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


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
