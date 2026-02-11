# Copyright 2020, Brigham Young University-Idaho. All rights reserved.

"""Interfaz gráfica para calcular el rango de frecuencia cardíaca
basado en la edad del usuario (50% y 85% del máximo).
"""
import tkinter as tk
from tkinter import Frame, Label, Button
from number_entry import IntEntry


def main():
    """Punto de entrada del programa."""
    root = tk.Tk()
    frm_main = Frame(root)
    frm_main.master.title("Frecuencia cardíaca")
    frm_main.pack(padx=4, pady=3, fill=tk.BOTH, expand=1)

    populate_main_window(frm_main)

    root.mainloop()


def populate_main_window(frm_main):
    """Organiza los widgets en la ventana principal: Labels, Entries y Botones.

    Parámetro:
        frm_main: el frame (ventana) principal.
    """
    # --- Widgets: Labels ---
    lbl_age = Label(frm_main, text="Edad (12 - 90):")
    lbl_age_units = Label(frm_main, text="años")
    lbl_rates = Label(frm_main, text="Rango (50% - 85%):")
    lbl_slow = Label(frm_main, width=4)
    lbl_fast = Label(frm_main, width=4)
    lbl_rate_units = Label(frm_main, text="latidos/min")
    lbl_status = Label(frm_main, text="", fg="gray", anchor="w")

    # --- Widget: IntEntry para la edad (solo números en rango) ---
    ent_age = IntEntry(frm_main, width=4, lower_bound=12, upper_bound=90)

    # --- Widgets: Botones ---
    btn_calculate = Button(frm_main, text="Calcular")
    btn_clear = Button(frm_main, text="Clear")

    # --- Layout con .grid() ---
    lbl_age.grid(row=0, column=0, padx=3, pady=3, sticky="e")
    ent_age.grid(row=0, column=1, padx=3, pady=3)
    lbl_age_units.grid(row=0, column=2, padx=0, pady=3, sticky="w")

    lbl_rates.grid(row=1, column=0, padx=3, pady=3, sticky="e")
    lbl_slow.grid(row=1, column=1, padx=3, pady=3)
    lbl_fast.grid(row=1, column=2, padx=3, pady=3)
    lbl_rate_units.grid(row=1, column=3, padx=0, pady=3, sticky="w")

    btn_calculate.grid(row=2, column=0, columnspan=2, padx=3, pady=3, sticky="w")
    btn_clear.grid(row=2, column=2, columnspan=2, padx=3, pady=3, sticky="w")

    lbl_status.grid(row=3, column=0, columnspan=4, padx=3, pady=3, sticky="ew")

    # --- Lógica de cálculo (50% y 85% del máximo: 220 - edad) ---
    def calculate(event=None):
        """Calcula y muestra el rango de frecuencia cardíaca (50% y 85%)."""
        try:
            age = ent_age.get()
            max_rate = 220 - age
            slow = max_rate * 0.50
            fast = max_rate * 0.85
            lbl_slow.config(text=f"{slow:.0f}")
            lbl_fast.config(text=f"{fast:.0f}")
            lbl_status.config(text="")
        except ValueError:
            lbl_slow.config(text="")
            lbl_fast.config(text="")
            lbl_status.config(
                text="Edad inválida. Debe ser un número entre 12 y 90.",
                fg="red"
            )

    def clear():
        """Limpia todos los campos y la barra de estado."""
        btn_clear.focus()
        ent_age.clear()
        lbl_slow.config(text="")
        lbl_fast.config(text="")
        lbl_status.config(text="")
        ent_age.focus()

    # --- Bindings y comandos ---
    ent_age.bind("<KeyRelease>", calculate)
    btn_calculate.config(command=lambda: calculate())
    btn_clear.config(command=clear)

    ent_age.focus()


if __name__ == "__main__":
    main()
