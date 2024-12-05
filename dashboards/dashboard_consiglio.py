import customtkinter as ctk
from tkinter import ttk, messagebox , Menu
import tkinter as tk
from Database_Utilities.connection import _connection
import os
import datetime
from datetime import datetime
from fpdf import FPDF
from PIL import Image, ImageTk
import fitz
import xml.etree.ElementTree as ET

def show_dashboard9(parent_frame):

    filter_frame = ctk.CTkFrame(parent_frame, corner_radius=5)
    filter_frame.pack(pady=5, padx=5, fill="x")
    global combobox

    selected_cliente = tk.StringVar()

    def setup_incremental_search(combobox, all_values):
        def filter_values():
            search_text = combobox.get().lower()
            filtered_values = [item for item in all_values if search_text in item.lower()]
            combobox['values'] = filtered_values if search_text else all_values
            if filtered_values:
                combobox.event_generate('<Down>')

        def on_keyrelease(event):
            # Schedule the filtering function to run after 500ms (or any other suitable delay)
            combobox.after_id = combobox.after(1000, filter_values)  # Delay of 500ms

        # Initialize after_id to manage subsequent calls
        combobox.after_id = None

        # Bind the on_keyrelease function to the KeyRelease event
        combobox.bind('<KeyRelease>', on_keyrelease)

    def get_unique_values(column_name):
        conn = _connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT DISTINCT `{column_name}` FROM `storico_ordini`")
        values = [row[0] for row in cursor.fetchall()]
        conn.close()
        return values

    def validate_date(date_text):
        try:
            return datetime.strptime(date_text, '%d-%m-%y').date()
        except ValueError:
            return None

    clienti = get_unique_values('cliente')
    fornitori = get_unique_values('fornitore')
    date = get_unique_values('data_ordine')
    id_ordine = get_unique_values('id_ordine')
    totale = get_unique_values('totale')
    prodotti = get_unique_values('prodotti')

    ctk.CTkLabel(filter_frame, text="Cliente:", font=('Arial', 14)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    cliente_combobox = ttk.Combobox(filter_frame, values=clienti, width=15, font=('Arial', 14))
    cliente_combobox.grid(row=0, column=1, padx=5, pady=5)
    cliente_combobox.option_add('*TCombobox*Listbox*Font', ('Arial', 14))
    setup_incremental_search(cliente_combobox, clienti)

    ctk.CTkLabel(filter_frame, text="Prodotti:", font=('Arial', 14)).grid(row=0, column=4, padx=5, pady=5, sticky="w")
    prodotti_combobox = ttk.Combobox(filter_frame, values=prodotti, width=15, font=('Arial', 14))
    prodotti_combobox.grid(row=0, column=5, padx=5, pady=5)
    prodotti_combobox.option_add('*TCombobox*Listbox*Font', ('Arial', 14))
    setup_incremental_search(prodotti_combobox, prodotti)

    ctk.CTkLabel(filter_frame, text="Movimenti:", font=('Arial', 14)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
    movimenti_combobox = ttk.Combobox(filter_frame, values=totale, width=15, font=('Arial', 14))
    movimenti_combobox.grid(row=1, column=1, padx=5, pady=5)
    movimenti_combobox.option_add('*TCombobox*Listbox*Font', ('Arial', 14))
    setup_incremental_search(movimenti_combobox, totale)

    ctk.CTkLabel(filter_frame, text="ID Ordine:", font=('Arial', 14)).grid(row=0, column=2, padx=5, pady=5, sticky="w")
    id_ordine_combobox = ttk.Combobox(filter_frame, values=id_ordine,width=15, font=('Arial', 14))
    id_ordine_combobox.grid(row=0, column=3, padx=5, pady=5)
    id_ordine_combobox.option_add('*TCombobox*Listbox*Font', ('Arial', 14))
    setup_incremental_search(id_ordine_combobox, id_ordine)

    ctk.CTkLabel(filter_frame, text="Start Date (DD-MM-YY):", font=('Arial', 14)).grid(row=0, column=6, padx=5, pady=5,sticky="w")
    start_date_entry = tk.Entry(filter_frame, width=12, font=('Arial', 14))
    start_date_entry.grid(row=0, column=7, padx=5, pady=5)

    ctk.CTkLabel(filter_frame, text="End Date (DD-MM-YY):", font=('Arial', 14)).grid(row=1, column=6, padx=5, pady=5,sticky="w")
    end_date_entry = tk.Entry(filter_frame, width=12, font=('Arial', 14))
    end_date_entry.grid(row=1, column=7, padx=5, pady=5)

    def apply_filters():
        start_date = validate_date(start_date_entry.get().strip())
        end_date = validate_date(end_date_entry.get().strip())

        filtered_orders = []
        for order in orders:
            order_date = datetime.strptime(order[1], '%Y-%m-%d').date()  # Make sure the format matches your data

            if (start_date is None or order_date >= start_date) and (end_date is None or order_date <= end_date):
                if (not id_ordine_combobox.get() or id_ordine_combobox.get() == str(order[0])) and \
                   (not cliente_combobox.get() or cliente_combobox.get().lower() in order[2].lower()) and \
                   (not prodotti_combobox.get() or prodotti_combobox.get().lower() in order[3].lower()) and \
                   (not movimenti_combobox.get() or movimenti_combobox.get() == str(order[4])):
                    filtered_orders.append(order)

        update_treeview(filtered_orders)


    ctk.CTkButton(filter_frame, text="Applica Filtri", command=apply_filters).grid(row=0, column=8, padx=10, pady=5)

    def clear_filters():
        start_date_entry.delete(0, tk.END)
        end_date_entry.delete(0, tk.END)

        # Clear all other combobox filters
        for combobox in [cliente_combobox,prodotti_combobox, movimenti_combobox, id_ordine_combobox]:
            combobox.set('')

        update_treeview(orders)  # Refresh or reset the view


    ctk.CTkButton(filter_frame, text="Rimuovi Filtri", command=clear_filters).grid(row=1, column=8, padx=10, pady=5)

    def copy_selection(tree):
        selected_items = tree.selection()  # Ottiene tutti gli elementi selezionati
        copied_data = []
        for item in selected_items:
            item_values = tree.item(item, "values")
            copied_data.append("\t".join(map(str, item_values)))  # Unisce i valori di ciascuna riga con una tabulazione
        clipboard_text = "\n".join(copied_data)  # Unisce tutte le righe con un ritorno a capo
        tree.clipboard_clear()  # Pulisce gli appunti
        tree.clipboard_append(clipboard_text)  # Aggiunge il testo agli appunti
        messagebox.showinfo("Copiato", "I testi selezionati sono stati copiati negli appunti.")

    def setup_context_menu(tree):
        # Creare un menu contestuale
        context_menu = Menu(tree, tearoff=0)
        context_menu.add_command(label="Copia", command=lambda: copy_selection(tree), font=('Arial', 14))

        def on_right_click(event):
            # Mostrare il menu contestuale
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()

        tree.bind("<Button-3>", on_right_click)  # <Button-3> è il clic del pulsante destro del mouse

    def on_mouse_drag(event):
        # Identifica l'item su cui si trova il cursore
        item = tree.identify_row(event.y)
        if item:
            tree.selection_add(item)

    table_frame = ctk.CTkFrame(parent_frame, corner_radius=5)
    table_frame.pack(pady=10, padx=10, fill="both", expand=True)

    columns = ("ID Ordine", "Data", "Cliente", "Prodotti", "Totale", "Fornitore")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    setup_context_menu(tree)
    tree.bind("<B1-Motion>", on_mouse_drag)

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

    scrollbar_x = ttk.Scrollbar(tree, orient=tk.HORIZONTAL, command=tree.xview)
    tree.configure(xscroll=scrollbar_x.set)
    scrollbar_x.pack(side="bottom", fill="x")

    tree.pack(side="left", fill="both", expand=True)

    def fetch_orders():
        conn = _connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM storico_ordini")
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


