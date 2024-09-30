import customtkinter as ctk
from tkinter import ttk, messagebox ,filedialog
import tkinter as tk
import sqlite3
import os
from fpdf import FPDF

def show_dashboard7(parent_frame):

    filter_frame = ctk.CTkFrame(parent_frame, corner_radius=5)
    filter_frame.pack(pady=10, padx=10, fill="x")

    def get_unique_values(column_name):
        conn = sqlite3.connect('resources/orders.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT DISTINCT {column_name} FROM orders")
        values = [row[0] for row in cursor.fetchall()]
        conn.close()
        return values

    clienti = get_unique_values('cliente')
    fornitori = get_unique_values('fornitore')
    date = get_unique_values('data')

    ctk.CTkLabel(filter_frame, text="Prodotto:", font=('Arial', 14)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    cliente_combobox = ttk.Combobox(filter_frame, values=clienti, state="readonly", width=20)
    cliente_combobox.grid(row=0, column=1, padx=10, pady=5)

    ctk.CTkLabel(filter_frame, text="Fornitore:", font=('Arial', 14)).grid(row=0, column=2, padx=10, pady=5, sticky="w")
    fornitore_combobox = ttk.Combobox(filter_frame, values=fornitori, state="readonly", width=20)
    fornitore_combobox.grid(row=0, column=3, padx=10, pady=5)

    ctk.CTkLabel(filter_frame, text="Data (YYYY-MM-DD):", font=('Arial', 14)).grid(row=0, column=4, padx=10, pady=5, sticky="w")
    data_combobox = ttk.Combobox(filter_frame, values=date, state="readonly", width=20)
    data_combobox.grid(row=0, column=5, padx=10, pady=5)

    def apply_filters():
        filtered_orders = [
            order for order in orders
            if (not cliente_combobox.get() or cliente_combobox.get().lower() in order[2].lower()) and
               (not fornitore_combobox.get() or fornitore_combobox.get().lower() in order[5].lower()) and
               (not data_combobox.get() or data_combobox.get() == order[1])
        ]
        update_treeview(filtered_orders)

    ctk.CTkButton(filter_frame, text="Applica Filtri", command=apply_filters).grid(row=0, column=6, padx=10, pady=5)

    table_frame = ctk.CTkFrame(parent_frame, corner_radius=5)
    table_frame.pack(pady=10, padx=10, fill="both", expand=True)

    columns = ("ID Ordine", "Data", "Cliente", "Prodotti", "Totale", "Fornitore")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")

    style = ttk.Style()
    style.configure("Treeview",
                    rowheight=30,
                    font=('Arial', 14),
                    background="#f1f8e9",
                    foreground="#004d40",
                    fieldbackground="#f1f8e9",
                    bordercolor="#000000",
                    relief="solid",
                    borderwidth=1)
    style.configure("Treeview.Heading",
                    font=('Arial', 16, 'bold'),
                    background="#a5d6a7",
                    foreground="#004d40")
    style.map("Treeview",
              background=[('selected', '#c8e6c9')],
              foreground=[('selected', '#004d40')])

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")
    tree.pack(pady=10, fill="both", expand=True)

    scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar_y.set)
    scrollbar_y.pack(side="right", fill="y")

    scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=tree.xview)
    tree.configure(xscroll=scrollbar_x.set)
    scrollbar_x.pack(side="bottom", fill="x")

    tree.pack(side="left", fill="both", expand=True)

    def fetch_orders():
        conn = sqlite3.connect('resources/orders.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
        conn.close()
        return orders

    orders = fetch_orders()

    def update_treeview(order_list):
        for row in tree.get_children():
            tree.delete(row)
        for order in order_list:
            tree.insert("", tk.END, values=order)

    update_treeview(orders)

