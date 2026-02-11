# W06 Final Project Milestone — CSE 111

Proyecto final (hito) de la semana 6 de CSE 111. Aplicación con interfaz gráfica (tkinter) y lógica separable para facilitar pruebas unitarias.

## Estructura del proyecto

- `README.md` — Este archivo
- `main.py` — Punto de entrada: ventana principal (GUI)
- `core.py` — Lógica de negocio (funciones puras, testeables)
- `number_entry.py` — Widgets IntEntry / FloatEntry para tkinter
- `test_core.py` — Pruebas unitarias con pytest

## Requisitos

- Python 3.10+ (o 3.8+)
- Solo biblioteca estándar (tkinter viene con Python).
- Para tests: `pytest` (opcional: `pip install pytest`).

## Cómo ejecutar la aplicación

```bash
python main.py
```

## Cómo ejecutar los tests

```bash
pytest test_core.py -v
```

## Convenciones

- **GUI**: prefijos `frm_`, `lbl_`, `ent_`, `btn_` para frames, labels, entries y botones.
- **Lógica**: en `core.py`, funciones puras que reciben datos y devuelven resultados (fácil de testear).
- **Tests**: en `test_core.py`, pruebas de las funciones de `core.py`.

## Archivos

- `main.py` — Ventana principal (calculadora de frecuencia cardíaca de ejemplo).

## Próximos pasos

1. Definir la funcionalidad concreta del proyecto (qué debe calcular o hacer la app).
2. Implementar las funciones en `core.py` y sus tests en `test_core.py`.
3. Conectar la GUI en `main.py` con las funciones de `core.py`.
