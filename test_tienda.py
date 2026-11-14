"""Pruebas de contrato para HU02 y validaciones HU01."""
from decimal import Decimal

import pytest

from tienda import calcular_total


def test_compra_con_descuento_normal():
    assert calcular_total("3333.00", 3, "10") == Decimal("8999.10")


def test_compra_sin_descuento():
    assert calcular_total("2500.00", 2, "0") == Decimal("5000.00")


def test_descuento_cien_por_ciento():
    assert calcular_total("100.00", 1, "100") == Decimal("0.00")


def test_precio_cero():
    assert calcular_total("0", 5, "20") == Decimal("0.00")


def test_redondeo_mitad_hacia_arriba():
    assert calcular_total("0.05", 1, "10") == Decimal("0.05")


def test_redondeo_solo_al_final():
    assert calcular_total("0.035", 3, "0") == Decimal("0.11")


def test_cantidad_minima_uno():
    assert calcular_total("12.00", 1, "0") == Decimal("12.00")


@pytest.mark.parametrize("precio,cantidad,descuento", [
    ("-10.00", 1, "0"),
    ("100", 0, "0"),
    ("100", 1, "101"),
    ("100", 1, "-1"),
    ("abc", 1, "0"),
    ("NaN", 1, "0"),
    ("Infinity", 1, "0"),
])
def test_valores_invalidos_generan_value_error(precio, cantidad, descuento):
    with pytest.raises(ValueError):
        calcular_total(precio, cantidad, descuento)


@pytest.mark.parametrize("precio,cantidad,descuento", [
    (100, 1, "0"),
    ("100", 1.5, "0"),
    ("100", True, "0"),
    ("100", 1, 10),
])
def test_tipos_invalidos_generan_type_error(precio, cantidad, descuento):
    with pytest.raises(TypeError):
        calcular_total(precio, cantidad, descuento)


def test_total_fuera_de_precision_genera_value_error():
    with pytest.raises(ValueError, match="El total supera la precisión disponible"):
        calcular_total("1e28", 1, "0")