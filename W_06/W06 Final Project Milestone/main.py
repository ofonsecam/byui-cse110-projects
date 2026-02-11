"""
W06 Final Project Milestone - Fons Inventory Management System
Creativity Enhancement:
I implemented a 'High Priority Purchase Report'. This feature cross-references
items with zero stock against a customer 'wishlist' to help the shop owner
(my father) prioritize which items to restock first based on actual demand.
"""
import tkinter as tk
from tkinter import Frame, Label, Button, Entry, messagebox
from number_entry import IntEntry
from core import (
    load_inventory,
    update_stock,
    save_inventory,
    add_product,
    delete_product,
    get_out_of_stock_requested,
)

INVENTORY_FILE = "inventory.csv"
pedidos_clientes = ["P001", "P002", "P004"]
lista_deseos = ["P002", "P004"]


def main():
    root = tk.Tk()
    frm_main = Frame(root)
    frm_main.master.title("Fons Inventory Management System")
    frm_main.pack(padx=8, pady=6, fill=tk.BOTH, expand=1)
    inventory = load_inventory(INVENTORY_FILE)
    populate_main_window(frm_main, inventory)
    root.mainloop()


def populate_main_window(frm_main, inventory):
    # --- Labels and entries ---
    lbl_product_id = Label(frm_main, text="ID del Producto (1-999):")
    lbl_name = Label(frm_main, text="Nombre (solo para registrar):")
    lbl_change = Label(frm_main, text="Cantidad / Cambio:")
    lbl_result = Label(frm_main, text="", width=36, anchor="w")
    lbl_status = Label(frm_main, text="", fg="gray", anchor="w")

    ent_product_id = IntEntry(frm_main, width=6, lower_bound=1, upper_bound=999)
    ent_name = Entry(frm_main, width=24)
    ent_change = IntEntry(frm_main, width=6, lower_bound=-10000, upper_bound=10000)

    # --- Buttons ---
    btn_update = Button(frm_main, text="Actualizar Stock")
    btn_clear = Button(frm_main, text="Clear")
    btn_add = Button(frm_main, text="Registrar Nuevo")
    btn_delete = Button(frm_main, text="Eliminar Producto")
    btn_report = Button(frm_main, text="Reporte de Faltantes Pedidos")
    btn_urgent = Button(frm_main, text="Ver Compras Urgentes")

    # --- Grid layout ---
    lbl_product_id.grid(row=0, column=0, padx=4, pady=3, sticky="e")
    ent_product_id.grid(row=0, column=1, padx=4, pady=3, sticky="w")
    lbl_name.grid(row=1, column=0, padx=4, pady=3, sticky="e")
    ent_name.grid(row=1, column=1, padx=4, pady=3, sticky="w")
    lbl_change.grid(row=2, column=0, padx=4, pady=3, sticky="e")
    ent_change.grid(row=2, column=1, padx=4, pady=3, sticky="w")
    lbl_result.grid(row=3, column=0, columnspan=2, padx=4, pady=4, sticky="w")
    # Row 4: update stock + clear
    btn_update.grid(row=4, column=0, padx=4, pady=3, sticky="w")
    btn_clear.grid(row=4, column=1, padx=4, pady=3, sticky="w")
    # Row 5: add + delete
    btn_add.grid(row=5, column=0, padx=4, pady=3, sticky="w")
    btn_delete.grid(row=5, column=1, padx=4, pady=3, sticky="w")
    # Row 6–7: reports
    btn_report.grid(row=6, column=0, columnspan=2, padx=4, pady=3, sticky="w")
    btn_urgent.grid(row=7, column=0, columnspan=2, padx=4, pady=3, sticky="w")
    lbl_status.grid(row=8, column=0, columnspan=2, padx=4, pady=4, sticky="ew")

    def clear_fields_and_status():
        """Clear all inputs and result; reset status text."""
        ent_product_id.clear()
        ent_name.delete(0, tk.END)
        ent_change.clear()
        lbl_result.config(text="")
        lbl_status.config(text="", fg="gray")

    def set_success(msg):
        """Show success message in lbl_status (green)."""
        clear_fields_and_status()
        lbl_status.config(text=msg, fg="green")

    def do_update(event=None):
        lbl_status.config(fg="gray")
        lbl_result.config(text="")
        try:
            product_id_num = ent_product_id.get()
            change = ent_change.get()
        except ValueError:
            lbl_status.config(text="Revisa ID y Cantidad.", fg="red")
            return
        product_id = f"P{product_id_num:03d}"
        try:
            update_stock(inventory, product_id, change)
            save_inventory(INVENTORY_FILE, inventory)
            name, qty = inventory[product_id]
            lbl_result.config(text=f"{name}: {qty}")
            set_success("Stock actualizado.")
        except KeyError as e:
            lbl_status.config(text=str(e), fg="red")
        except ValueError as e:
            lbl_status.config(text=str(e), fg="red")

    def do_add():
        """Register new product: ID (P prefix), name, quantity → add_product → save_inventory."""
        lbl_status.config(fg="gray")
        lbl_result.config(text="")
        try:
            product_id_num = ent_product_id.get()
            quantity = ent_change.get()
        except ValueError:
            lbl_status.config(text="Revisa ID y Cantidad (número válido).", fg="red")
            return
        name = ent_name.get().strip()
        if not name:
            lbl_status.config(text="Escribe el nombre del producto.", fg="red")
            return
        product_id = f"P{product_id_num:03d}"
        try:
            add_product(inventory, product_id, name, quantity)
            save_inventory(INVENTORY_FILE, inventory)
            set_success("Producto registrado.")
        except ValueError as e:
            lbl_status.config(text=str(e), fg="red")

    def do_delete():
        """Remove product by ID: delete_product → save_inventory."""
        lbl_status.config(fg="gray")
        lbl_result.config(text="")
        try:
            product_id_num = ent_product_id.get()
        except ValueError:
            lbl_status.config(text="Revisa ID del producto.", fg="red")
            return
        product_id = f"P{product_id_num:03d}"
        try:
            delete_product(inventory, product_id)
            save_inventory(INVENTORY_FILE, inventory)
            set_success("Producto eliminado.")
        except KeyError as e:
            lbl_status.config(text=str(e), fg="red")

    def clear():
        btn_clear.focus()
        clear_fields_and_status()
        ent_product_id.focus()

    def show_missing_report():
        urgentes = get_out_of_stock_requested(inventory, pedidos_clientes)
        if urgentes:
            msg = f"Productos urgentes por comprar: {', '.join(urgentes)}"
        else:
            msg = "Todo el stock solicitado está al día"
        win = tk.Toplevel(frm_main.winfo_toplevel())
        win.title("Reporte de Faltantes Pedidos")
        win.geometry("420x80")
        Label(win, text=msg, wraplength=380, justify=tk.LEFT, padx=10, pady=10).pack(
            anchor="w", fill=tk.BOTH, expand=True
        )
        Button(win, text="Cerrar", command=win.destroy).pack(pady=(0, 10))

    def show_urgent_purchases():
        faltantes = get_out_of_stock_requested(inventory, lista_deseos)
        if faltantes:
            msg = f"Productos agotados de la lista de deseos: {', '.join(faltantes)}"
        else:
            msg = "Inventario al día"
        messagebox.showinfo("Compras Urgentes", msg)

    btn_update.config(command=do_update)
    btn_clear.config(command=clear)
    btn_add.config(command=do_add)
    btn_delete.config(command=do_delete)
    btn_report.config(command=show_missing_report)
    btn_urgent.config(command=show_urgent_purchases)
    ent_product_id.focus()


if __name__ == "__main__":
    main()
