# Informe de revisión de código y seguridad

**Proyecto:** Tienda local  
**Estudiante:** Juan David Alvarado Cuéllar  
**Fecha:** 14 de noviembre de 2026  
**Commit revisado:** `11fcbcb`

## 1. Herramientas y criterios

Ruff 0.17.5 revisó las reglas E, F, B y S. Después de configurar la excepción de S101 para el archivo de pruebas, el resultado fue `All checks passed!`. Con pytest 9.2.0 pasaron las 19 pruebas.

| Punto | Resultado |
|---|---|
| Inyección | El programa convierte los argumentos en números. No ejecuta consultas SQL ni comandos del sistema con esos datos. |
| Secretos | La búsqueda de patrones de credenciales en los cuatro commits del ZIP original no arrojó coincidencias. `.gitignore` excluye `.env` y permite `.env.example`. |
| Contraseñas | No aplica. El programa no autentica usuarios ni guarda contraseñas. |
| Control de acceso | No aplica. La calculadora funciona de forma local y no tiene cuentas ni roles. |
| Dependencias | Pytest se utiliza para las pruebas. `pip-audit` 2.10.1 reportó `No known vulnerabilities found` al revisar `requirements.txt`. |

## 2. Hallazgos

| ID | Archivo y línea en la base | Problema | Categoría | Severidad | Corrección | Commit |
|---|---|---|---|---|---|---|
| H-01 | `tienda.py`, líneas 35 a 37 | El precio `1e28` genera `decimal.InvalidOperation` al redondear. | Manejo de errores | Media | Se convierte el fallo en `ValueError` y se agrega una prueba de regresión. | `62c0836` |
| H-02 | `test_tienda.py`, líneas 10, 14, 18, 22, 26, 30 y 34 | Ruff marca siete usos de `assert` con S101. | Linter | Baja | Se permite S101 únicamente en `test_tienda.py`, donde los `assert` comprueban los resultados. | Pendiente de registrar `pyproject.toml` en Git. |

## 3. Revisión con IA

Se usó ChatGPT para revisar el manejo de entradas y errores, además de interpretar los avisos de Ruff.

| Observación | Clasificación | Verificación |
|---|---|---|
| Una entrada decimal finita puede causar una excepción al redondear. | Real | Se reprodujo con `python tienda.py --precio 1e28 --cantidad 1 --descuento 0`. Después de la corrección pasó la prueba nueva. |
| Los avisos S101 podrían indicar validaciones de seguridad hechas con `assert`. | Falso positivo como riesgo del programa | Los siete `assert` están en las pruebas. La función `validar_entrada` usa condiciones y excepciones. |

La revisión inicial omitió que la consola admite abreviaturas. Se comprobó que `--pre 100 --cant 1 --desc 0` devuelve `100.00` en la versión base.

## 4. Pendientes

- Registrar el commit de Ruff en la fila H-02.
- Confirmar que `requirements.txt` fija `pytest==9.2.0`.
- Revisar las ramas locales adicionales, si las hay. La búsqueda de credenciales cubrió el historial del ZIP original.