# Tienda local

## Qué es
Calculadora de consola en Python que obtiene el total de una compra a partir
del precio unitario, la cantidad y el porcentaje de descuento. Valida las
entradas y redondea el total a dos decimales.

## Requisitos
Python 3.10 o superior. La calculadora usa la biblioteca estándar de Python.
Pytest se usa para las pruebas y Ruff para revisar el código.

## Instalación
Ejecuta estos comandos en PowerShell desde la carpeta que contiene `tienda.py`.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt "ruff==0.17.5"
```

## Ejecución
```powershell
.\.venv\Scripts\python.exe tienda.py --precio 3333.00 --cantidad 3 --descuento 10
```

Resultado esperado: `8999.10`. Usa punto para los decimales, una cantidad
entera mayor o igual a 1 y un descuento entre 0 y 100.

## Pruebas
```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check .
```

## Estructura
- `tienda.py`: validación, cálculo y ejecución por consola.
- `test_tienda.py`: pruebas del cálculo y de las entradas inválidas.
- `requirements.txt` y `pyproject.toml`: versión de Pytest y configuración de Ruff.
- `revision_seguridad.md` y `bitacora_ia.md`: informe y registro del uso de IA.

## Uso de IA
Usé ChatGPT para revisar el cálculo, entender los avisos de Ruff y proponer
una prueba para el error de precisión. Comprobé la corrección con Pytest
y registré los resultados en el informe.

## Autor y licencia
Juan David Alvarado Cuéllar. Proyecto académico del Seminario en Inteligencia
Artificial Aplicada al Ciclo de Vida del Software. Sin licencia indicada.