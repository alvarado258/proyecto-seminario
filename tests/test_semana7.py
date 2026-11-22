import sys
from decimal import Decimal

import pytest

from tienda import calcular_total, main, validar_entrada


@pytest.fixture
def compra_sintetica():
    """Precio unitario y cantidad de una compra ficticia."""
    return "1000.00", 2


@pytest.mark.parametrize(
    "descuento, esperado",
    [
        ("0", "2000.00"),    # Límite mínimo válido.
        ("10", "1800.00"),   # Descuento normal.
        ("99.99", "0.20"),   # Justo por debajo del máximo.
        ("100", "0.00"),     # Límite máximo válido.
    ],
)
def test_total_segun_descuento(compra_sintetica, descuento, esperado):
    precio, cantidad = compra_sintetica
    total = calcular_total(precio, cantidad, descuento)
    assert total == pytest.approx(
        Decimal(esperado), rel=0, abs=Decimal("0")
    )


def test_rechaza_descuento_superior_al_maximo(compra_sintetica):
    precio, cantidad = compra_sintetica
    with pytest.raises(ValueError):
        calcular_total(precio, cantidad, "100.01")


def test_rechaza_descuento_negativo(compra_sintetica):
    precio, cantidad = compra_sintetica
    with pytest.raises(ValueError):
        calcular_total(precio, cantidad, "-0.01")


def test_acepta_cantidad_minima():
    datos = validar_entrada("1000.00", 1, "10")
    assert datos["cantidad"] == 1


@pytest.mark.parametrize(
    "cantidad, error_esperado",
    [
        (0, ValueError),    # Entero fuera del rango.
        (True, TypeError),  # Tipo de dato incorrecto.
    ],
)
def test_rechaza_cantidad_invalida(cantidad, error_esperado):
    with pytest.raises(error_esperado):
        validar_entrada("1000.00", cantidad, "10")


def test_main_muestra_total(monkeypatch, capsys):
    monkeypatch.setattr(
        sys, "argv",
        ["tienda.py", "--precio", "1000.00", "--cantidad", "2", "--descuento", "10"],
    )
    assert main() == 0
    assert capsys.readouterr().out.strip() == "1800.00"


def test_main_informa_cantidad_invalida(monkeypatch, capsys):
    monkeypatch.setattr(
        sys, "argv",
        ["tienda.py", "--precio", "1000.00", "--cantidad", "0", "--descuento", "10"],
    )
    assert main() == 1
    salida = capsys.readouterr()
    assert "cantidad" in (salida.out + salida.err).lower()