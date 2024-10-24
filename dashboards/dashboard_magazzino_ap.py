import os
from tkinter.filedialog import asksaveasfilename

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, Menu
import sqlite3
import openpyxl
import pandas as pd
from Database_Utilities.crud_fornitori import get_all_prodotti
# Import CRUD functions for Andria
from Database_Utilities.crud_andria import read_records_andria, update_record_andria, delete_record_andria
from Database_Utilities.crud_andria import transfer_quantity_from_andria_to_parigi
from Database_Utilities.crud_clienti import get_all_clienti_names
# Import CRUD functions for Parigi
from Database_Utilities.crud_parigi import read_records_parigi, update_record_parigi, delete_record_parigi


def aggiungi_prodotto():
    dialog = tk.Toplevel()
    dialog.title("Scegli Azione")
    dialog.grab_set()
    dialog.transient()

    # Etichetta per il menu a tendina
    label_prodotto = tk.Label(dialog, text="Scegli Prodotto:", font=("Arial", 14))
    label_prodotto.pack(pady=10)

    # Funzione per aggiornare il menu a tendina in base al testo digitato
    def update_combobox(event):
        prodotti_aggiornati = get_all_prodotti()
        typed_text = combobox_prodotto.get()
        prodotti_filtrati = [prod for prod in prodotti_aggiornati if typed_text.lower() in prod.lower()]
        cursor_position = combobox_prodotto.index(tk.INSERT)
        combobox_prodotto['values'] = prodotti_filtrati
        combobox_prodotto.set(typed_text)
        combobox_prodotto.icursor(cursor_position)
        combobox_prodotto.event_generate('<Down>')

    # Funzione per ottenere la composizione cartone e il codice del prodotto
    def get_product_info(prodotto_descrizione):
        conn = sqlite3.connect("Database_Utilities/Database/MergedDatabase.db")
        cursor = conn.cursor()
        cursor.execute("SELECT Codice, COMPOSIZIONE_CARTONE FROM prodotti WHERE Descrizione = ?", (prodotto_descrizione,))
        result = cursor.fetchone()
        conn.close()
        return result if result else (None, None)

    # Funzione per inserire o aggiornare il prodotto nella tabella Andria o Parigi
    def update_or_insert_in_table(codice, quantita, cartoni, tabella):
        conn = sqlite3.connect("Database_Utilities/Database/MergedDatabase.db")
        cursor = conn.cursor()

        # Verifica se il prodotto esiste già nella tabella
        cursor.execute(f"SELECT Esistenze, Cartoni FROM {tabella} WHERE Codice = ?", (codice,))
        result = cursor.fetchone()

        if result:
            # Aggiorna le quantità e i cartoni
            esistenze_correnti, cartoni_correnti = result
            nuove_esistenze = esistenze_correnti + quantita
            nuovi_cartoni = nuove_esistenze // cartoni if cartoni > 0 else 0
            cursor.execute(f"UPDATE {tabella} SET Esistenze = ?, Cartoni = ? WHERE Codice = ?", (nuove_esistenze, nuovi_cartoni, codice))
        else:
            # Inserisci una nuova riga
            cursor.execute(f"INSERT INTO {tabella} (Codice, Esistenze, Cartoni) VALUES (?, ?, ?)", (codice, quantita, cartoni))

        conn.commit()
        conn.close()

    # Creazione del menu a tendina per selezionare il prodotto
    prodotti = get_all_prodotti()
    prodotto_selezionato = tk.StringVar()
    combobox_prodotto = ttk.Combobox(dialog, textvariable=prodotto_selezionato, values=prodotti, font=("Arial", 14))
    combobox_prodotto.configure(width=35)
    combobox_prodotto.option_add('*TCombobox*Listbox*Font', ('Arial', 16))
    combobox_prodotto.pack(pady=5)
    combobox_prodotto.bind("<KeyRelease>", update_combobox)

    # Selettore per "Andria" o "Parigi"
    label_selezione = tk.Label(dialog, text="Seleziona la sede:", font=("Arial", 14))
    label_selezione.pack(pady=10)
    selezione_sede = tk.StringVar(value="andria")  # Default "andria"
    sede_andria = tk.Radiobutton(dialog, text="Andria", variable=selezione_sede, value="andria", font=("Arial", 14))
    sede_parigi = tk.Radiobutton(dialog, text="Parigi", variable=selezione_sede, value="parigi", font=("Arial", 14))
    sede_andria.pack()
    sede_parigi.pack()

    # Campo per la quantità
    label_quantita = tk.Label(dialog, text="Inserisci Quantità:", font=("Arial", 14))
    label_quantita.pack(pady=10)
    quantita_entry = tk.Entry(dialog, font=("Arial", 14))
    quantita_entry.pack(pady=5)

    # Funzione per gestire il salvataggio dei dati
    def on_confirm():
        prodotto_descrizione = prodotto_selezionato.get()
        quantita = quantita_entry.get()

        if not quantita.isdigit():
            messagebox.showerror("Errore", "Inserisci un valore numerico valido per la quantità.")
            return

        quantita = int(quantita)

        # Ottieni il codice del prodotto e la composizione cartone
        codice_prodotto, composizione_cartone = get_product_info(prodotto_descrizione)

        if codice_prodotto is None or composizione_cartone is None:
            messagebox.showerror("Errore", "Prodotto non trovato nel database.")
            return

        composizione_cartone = int(composizione_cartone) if composizione_cartone.isdigit() else 1
        cartoni = quantita // composizione_cartone if composizione_cartone > 0 else 0

        # Ottieni la sede selezionata e aggiorna/inserisci nella tabella corretta
        sede = selezione_sede.get()
        update_or_insert_in_table(codice_prodotto, quantita, cartoni, sede)

        messagebox.showinfo("Prodotto Aggiunto", f"Hai aggiunto {quantita} unità di '{prodotto_descrizione}' ({cartoni} cartoni) a {sede.capitalize()}.")
        dialog.destroy()

    # Bottone di conferma per aggiungere il prodotto
    button_confirm = tk.Button(dialog, text="Conferma", font=("Arial", 14), command=on_confirm)
    button_confirm.pack(pady=10)









def center_window(window, width, height):
    window.update_idletasks()
    width = width
    height = height
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

button_font = ("Arial", 12)  # Font più grande per i pulsanti
button_width = 15  # Larghezza maggiore per i pulsanti
button_height = 2  # Altezza maggiore per i pulsanti

def get_city_info(city):
    if city == 'andria':
        info = read_records_andria()
    elif city == 'parigi':
        info = read_records_parigi()
    return info

def show_info(city, tree, table_frame):
    # Connect to the merged database
    conn = sqlite3.connect('Database_Utilities/Database/MergedDatabase.db')
    c = conn.cursor()

    # Fetch data based on the selected city
    if city == "andria":
        c.execute("""
                SELECT 
                    p.Codice, 
                    p.Descrizione, 
                    p.COMPOSIZIONE_CARTONE, 
                    f.Nome, 
                    e.Esistenze, 
                    e.Cartoni
                FROM prodotti p
                JOIN fornitori f ON p.ID_FORNITORE = f.id
                JOIN andria e ON p.Codice = e.Codice
            """)
    elif city == "parigi":
        c.execute("""
                SELECT 
                    p.codice, 
                    p.descrizione, 
                    p.composizione_cartone, 
                    f.nome, 
                    e.esistenze, 
                    e.cartoni
                FROM prodotti p
                JOIN fornitori f ON p.id_fornitore = f.id
                JOIN parigi e ON p.codice = e.codice
            """)

    data = c.fetchall()
    conn.close()

    # Clear the current TreeView
    for row in tree.get_children():
        tree.delete(row)

    # Insert new data into the TreeView
    for row in data:
        tree.insert("", tk.END, values=row)

    # Display the updated table
    tree.city = city  # Save the current city in the tree
    table_frame.pack(pady=10, fill="both", expand=True)

def show_action_dialog(product_name, city, callback):
    dialog = tk.Toplevel()
    dialog.title("Scegli Azione")
    dialog.grab_set()  # Ottieni il focus sulla finestra di dialogo
    dialog.transient()  # Rendi la finestra di dialogo modale

    if city == 'andria':
        label = tk.Label(dialog, text=f"Vuoi inserire una nuova quantità, eliminare o spostare '{product_name}'?",
                         font=("Arial", 16))
        label.pack(pady=10)

    elif city == 'parigi':
        label = tk.Label(dialog, text=f"Vuoi inserire una nuova quantità, eliminare o vendere '{product_name}'?",
                         font=("Arial", 16))
        label.pack(pady=10)

    button_frame = tk.Frame(dialog)
    button_frame.pack(pady=10)

    def on_modify():
        dialog.destroy()
        callback("modify")

    def on_delete():
        dialog.destroy()
        callback("delete")

    def on_move():
        dialog.destroy()
        callback("move")

    def on_sold():
        dialog.destroy()
        callback("sold")

    modify_button = tk.Button(button_frame, text="Nuova quantità", font=button_font, width=button_width,
                              height=button_height, command=on_modify)
    modify_button.grid(row=0, column=0, padx=10, pady=10)

    delete_button = tk.Button(button_frame, text="Elimina", font=button_font, width=button_width, height=button_height,
                              command=on_delete)
    delete_button.grid(row=0, column=1, padx=10, pady=10)

    if city == 'andria':
        move_button = tk.Button(button_frame, text="Sposta a Parigi", font=button_font, width=button_width,
                                height=button_height, command=on_move)
        move_button.grid(row=0, column=2, padx=10, pady=10)

    elif city == 'parigi':
        move_button = tk.Button(button_frame, text="Venduto", font=button_font, width=button_width,
                                height=button_height, command=on_sold)
        move_button.grid(row=0, column=2, padx=10, pady=10)

    center_window(dialog,600,300)
    dialog.wait_window()  # Attendi la chiusura della finestra di dialogo

def ask_details(product,city,action, prompt, current_esistenze, current_cartoni):
    dialog = tk.Toplevel()
    dialog.title("Dettagli Prodotto")
    dialog.grab_set()
    dialog.transient()

    label = tk.Label(dialog, text=prompt, font=("Arial", 14))
    label.pack(pady=10)

    # Inizializza i campi con i valori correnti
    quantity_var = tk.IntVar(value=current_esistenze)
    cartons_var = tk.IntVar(value=current_cartoni)

    quantity_label = tk.Label(dialog, text=f"Quantità di '{product}':",  font= ("Arial", 14))
    quantity_label.pack(pady=5)
    quantity_entry = tk.Entry(dialog, textvariable=quantity_var, font=("Arial", 14))
    quantity_entry.pack(pady=5)

    cartons_label = tk.Label(dialog, text=f"Cartoni di '{product}':", font=("Arial", 14))
    cartons_label.pack(pady=5)
    cartons_entry = tk.Entry(dialog, textvariable=cartons_var,  font=("Arial", 14))
    cartons_entry.pack(pady=5)

    if city == 'parigi' and action == 'sold':
        # Crea il menu a tendina per selezionare il prodotto
        clienti = get_all_clienti_names()  # Da modificare
        cliente_selezionato = tk.StringVar()
        cliente_label = tk.Label(dialog, text=f"Cliente:", font=("Arial", 14))
        cliente_label.pack(pady=5)
        clienti_prodotto = ttk.Combobox(dialog, textvariable=cliente_selezionato, values=clienti, font=("Arial", 14))
        clienti_prodotto.configure(width=35)
        clienti_prodotto.option_add('*TCombobox*Listbox*Font', ('Arial', 16))
        clienti_prodotto.pack(pady=5)


    def on_confirm():
        dialog.destroy()
        if city == 'parigi' and action == 'sold':
            dialog.details = {'quantity': quantity_var.get(), 'cartons': cartons_var.get(), 'cliente': cliente_selezionato.get()}
        else:
            dialog.details = {'quantity': quantity_var.get(), 'cartons': cartons_var.get()}

    confirm_button = tk.Button(dialog, text="Conferma",  font=("Arial", 12) , command=on_confirm)
    confirm_button.pack(pady=10)

    center_window(dialog,600,400)
    dialog.wait_window()
    return getattr(dialog, 'details', None)
def handle_action(action, product,current_esistenze, current_cartoni, city, tree):
    if city == 'andria':
        if action == "modify":
            details = ask_details(product,city,action, f"Inserisci la nuova quantità e i cartoni per '{product}':", current_esistenze, current_cartoni)
            if details and details['quantity'] is not None:
                update_record_andria(product, details['quantity'], details['cartons'])
                show_info(city, tree, tree.table_frame)
                messagebox.showinfo("Aggiunta Prodotto", f"Hai aggiunto {details['quantity']} prodotti di '{product}'.")
        elif action == "delete":
            confirm = messagebox.askokcancel("Conferma Eliminazione", f"Sei sicuro di voler eliminare '{product}'?")
            if confirm:
                delete_record_andria(product)
                show_info(city, tree, tree.table_frame)
                messagebox.showinfo("Eliminazione Prodotto", f"Il prodotto '{product}' è stato eliminato.")
        elif action == "move":
            details = ask_details(product,city,action, f"Inserisci la quantità e i cartoni da spostare per '{product}':",current_esistenze, current_cartoni)
            if details and details['quantity'] is not None:
                confirm = messagebox.askokcancel("Conferma Spostamento", f"Sei sicuro di voler spostare {details['quantity']} di '{product}'?")
                if confirm:
                    transfer_quantity_from_andria_to_parigi(product, details['quantity'])
                    show_info(city, tree, tree.table_frame)
                    messagebox.showinfo("Spostamento Prodotto", f"Il prodotto '{product}' è stato spostato.")
    elif city == 'parigi':
        if action == "modify":
            details = ask_details(product,city,action, f"Inserisci la nuova quantità e i cartoni per '{product}':", current_esistenze, current_cartoni)
            if details and details['quantity'] is not None:
                update_record_parigi(product, details['quantity'], details['cartons'])
                show_info(city, tree, tree.table_frame)
                messagebox.showinfo("Aggiunta Prodotto", f"Hai modificato {details['quantity']} prodotti di '{product}'.")
        elif action == "delete":
            confirm = messagebox.askokcancel("Conferma Eliminazione", f"Sei sicuro di voler eliminare '{product}'?")
            if confirm:
                delete_record_parigi(product)
                show_info(city, tree, tree.table_frame)
                messagebox.showinfo("Eliminazione Prodotto", f"Il prodotto '{product}' è stato eliminato.")
        elif action == "sold":
            details = ask_details(product,city,action, f"Inserisci la quantità venduta, i cartoni e il cliente per '{product}':", current_esistenze, current_cartoni)
            if details and details['quantity'] is not None and details['cliente'] is not None:
                confirm = messagebox.askokcancel("Conferma Venduto", f"Sei sicuro di voler spostare in venduti '{product}'?")
                if confirm:
                    update_record_parigi(product, details['quantity'], details['cartons'],details['cliente'])
                    #aggiungere funzione per mandare ordine in storico ordini
                    show_info(city, tree, tree.table_frame)
                    messagebox.showinfo("Prodotto Venduto", f"Il prodotto '{product}' è stato venduto.")

def on_double_click(event, tree):
    item = tree.selection()[0]
    values = tree.item(item, "values")
    if values:
        city = tree.city  # Recupera la città salvata
        product = values[0]
        current_esistenze = values[4]
        current_cartoni = values[5]
        show_action_dialog(product, city, lambda action: handle_action(action, product,current_esistenze, current_cartoni, city, tree))

def generate_excel():
    dialog = tk.Toplevel()
    dialog.title("Seleziona Città")
    dialog.grab_set()
    dialog.transient()

    label = tk.Label(dialog, text="Scegli la città per generare il report Excel:", font=("Arial", 16))
    label.pack(pady=20)

    def on_city_selected(city):
        dialog.destroy()
        export_data_to_excel(city)

    button_andria = tk.Button(dialog, text="Andria", font=button_font, width=button_width,
                              height=button_height,
                              command=lambda: on_city_selected('andria'))
    button_andria.pack(pady=10)

    button_parigi = tk.Button(dialog, text="Parigi", font=button_font, width=button_width,
                              height=button_height,
                              command=lambda: on_city_selected('parigi'))
    button_parigi.pack(pady=10)

    # Configura le dimensioni e la posizione del popup
    center_window(dialog,600,300)  # Imposta le dimensioni desiderate per il popup
    dialog.wait_window()

def export_data_to_excel(city):
    # Connect to the merged database
    conn = sqlite3.connect('dashboards/Database_Utilities/MergedDatabase.db')
    c = conn.cursor()

    # SQL query to fetch data based on the selected city (andria or parigi)
    if city == "andria":
        c.execute("""
            SELECT 
                p.codice, 
                p.descrizione, 
                p.composizione_cartone, 
                f.nome, 
                e.esistenze, 
                e.cartoni
            FROM prodotti p
            JOIN fornitori f ON p.id_fornitore = f.id
            JOIN andria e ON p.codice = e.codice
        """)
    elif city == "parigi":
        c.execute("""
            SELECT 
                p.codice, 
                p.descrizione, 
                p.composizione_cartone, 
                f.nome, 
                e.esistenze, 
                e.cartoni
            FROM prodotti p
            JOIN fornitori f ON p.id_fornitore = f.id
        """)

    # Fetch the data
    data = c.fetchall()
    conn.close()


    # Save the data to Excel
    if not data:
        messagebox.showwarning("Nessun Dato", f"Nessun dato trovato per la città '{city}'.")
        return

    default_filename = f"Esistenze_{city}_data.xlsx"
    file_path = asksaveasfilename(defaultextension=".xlsx",
                                  filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                                  initialfile=default_filename)

    if not file_path:
        messagebox.showwarning("Salvataggio Annullato", "Salvataggio del file Excel annullato.")
        return

    # Create Excel file and save
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = f"Esistenze {city}"

    headers = ["Codice", "Descrizione", "Composizione Cartone", "Fornitore", "Esistenti", "Cartoni"]
    sheet.append(headers)

    for row in data:
        sheet.append(row)

    workbook.save(file_path)
    messagebox.showinfo("Excel Generato", f"Il file Excel è stato salvato come '{os.path.basename(file_path)}'")

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
    context_menu.add_command(label="Copia", command=lambda: copy_selection(tree), font=("Arial", 14))

    def on_right_click(event):
        # Mostrare il menu contestuale
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    tree.bind("<Button-3>", on_right_click)  # <Button-3> è il clic del pulsante destro del mouse

# Aggiungere il supporto per la selezione trascinando
def on_mouse_drag(event):
    # Identifica l'item su cui si trova il cursore
    item = tree.identify_row(event.y)
    if item:
        tree.selection_add(item)

def setup_treeview(tree):
    columns = ("CODICE", "DESCRIZIONE", "COMPOSIZIONE CARTONE", "FORNITORE", "ESISTENTI", "CARTONI")
    tree['columns'] = columns

    # Initialize sorting order tracking
    sort_order = {col: False for col in columns}  # False = Ascending, True = Descending

    # Set up column headings with sorting functionality
    tree.heading("CODICE", text="CODICE", anchor="w",
                 command=lambda: treeview_sort_column(tree, "CODICE", sort_order["CODICE"]))
    tree.heading("DESCRIZIONE", text="DESCRIZIONE", anchor="w",
                 command=lambda: treeview_sort_column(tree, "DESCRIZIONE", sort_order["DESCRIZIONE"]))
    tree.heading("COMPOSIZIONE CARTONE", text="COMPOSIZIONE CARTONE", anchor="w",
                 command=lambda: treeview_sort_column(tree, "COMPOSIZIONE CARTONE", sort_order["COMPOSIZIONE CARTONE"]))
    tree.heading("FORNITORE", text="FORNITORE", anchor="w",
                 command=lambda: treeview_sort_column(tree, "FORNITORE", sort_order["FORNITORE"]))
    tree.heading("ESISTENTI", text="ESISTENTI", anchor="w",
                 command=lambda: treeview_sort_column(tree, "ESISTENTI", sort_order["ESISTENTI"]))
    tree.heading("CARTONI", text="CARTONI", anchor="w",
                 command=lambda: treeview_sort_column(tree, "CARTONI", sort_order["CARTONI"]))

    # Set up column widths and other configurations as before
    tree.column("CODICE", width=120, anchor="center")
    tree.column("DESCRIZIONE", width=200, anchor="center")
    tree.column("COMPOSIZIONE CARTONE", width=150, anchor="center")
    tree.column("FORNITORE", width=150, anchor="center")
    tree.column("ESISTENTI", width=120, anchor="center")
    tree.column("CARTONI", width=100, anchor="center")

    def treeview_sort_column(tree, col, col_type):
        """Funzione per ordinare le colonne."""
        nonlocal sort_order
        reverse = sort_order[col]
        # Determina il tipo di dato per corretta comparazione nel sort
        if col_type == 'number':
            converter = float
        else:
            converter = str

        l = [(tree.set(k, col), k) for k in tree.get_children('')]
        l.sort(reverse=reverse, key=lambda x: converter(x[0]))

        for index, (val, k) in enumerate(l):
            tree.move(k, '', index)

        sort_order[col] = not reverse
        tree.heading(col, text=col, command=lambda: treeview_sort_column(tree, col, col_type))

    tree.heading("CODICE", text="CODICE", anchor="w",
                 command=lambda: treeview_sort_column(tree, "CODICE", 'text'))
    tree.heading("ESISTENTI", text="ESISTENTI", anchor="w",
                 command=lambda: treeview_sort_column(tree, "ESISTENTI", 'number'))
    tree.heading("CARTONI", text="CARTONI", anchor="w",
                 command=lambda: treeview_sort_column(tree, "CARTONI", 'number'))

    tree.column("CODICE", width=120, anchor="center")
    tree.column("ESISTENTI", width=150, anchor="center")
    tree.column("CARTONI", width=120, anchor="center")

def show_dashboard1(parent_frame):
    parent_frame_color = parent_frame.cget("fg_color")

    # Crea un frame per contenere sia il titolo che la legenda
    top_frame = ctk.CTkFrame(parent_frame, corner_radius=5, fg_color=parent_frame_color)
    top_frame.pack(fill="x", pady=0)  # Si espande orizzontalmente

    # Usa il layout grid nel top_frame
    top_frame.columnconfigure(0, weight=0)  # La colonna 0 non si espande
    top_frame.columnconfigure(1, weight=1)  # La colonna 1 si espande

    # Aggiungi l'etichetta "Scegli una città" all'interno del top_frame, allineata a sinistra
    label = ctk.CTkLabel(top_frame, text="Scegli una città:", font=('Arial', 14))
    label.grid(row=0, column=1, padx=10)

    # Aggiungi la legenda all'interno del top_frame, allineata a destra
    legend_label = ctk.CTkLabel(top_frame, text="Unità di misura:\n- L: liters\n- Kg: kilograms\n- Pz: pieces",
                                font=('Arial', 12), justify="left")
    legend_label.grid(row=0, column=0, sticky="w", padx=10)

    button_frame = ctk.CTkFrame(parent_frame, corner_radius=5)
    button_frame.pack(pady=0)

    button_andria = ctk.CTkButton(button_frame, text="Andria", command=lambda: show_info("andria", tree, table_frame), corner_radius=5)
    button_andria.grid(row=0, column=0, padx=10)

    button_paris = ctk.CTkButton(button_frame, text="Parigi", command=lambda: show_info("parigi", tree, table_frame), corner_radius=5)
    button_paris.grid(row=0, column=1, padx=10)

    button_excel = ctk.CTkButton(button_frame, text="Stampa Excel", command=generate_excel, corner_radius=5)
    button_excel.grid(row=0, column=2, padx=10)

    button_add_products = ctk.CTkButton(button_frame, text="Aggiungi prodotto", command= aggiungi_prodotto, corner_radius=5)
    button_add_products.grid(row=0, column=2, padx=10)

    global table_frame
    table_frame = ctk.CTkFrame(parent_frame, corner_radius=5)
    table_frame.pack_forget()

    global columns
    columns = ("CODICE", "ESISTENTI", "CARTONI")
    global tree
    tree = ttk.Treeview(table_frame, columns=columns,style="dash1.Treeview",show="headings")
    tree.table_frame = table_frame  # Salva il frame nella treeview per riferimento
    setup_treeview(tree)
    setup_context_menu(tree)
    tree.bind("<B1-Motion>", on_mouse_drag)

    style = ttk.Style()
    style.configure("dash1.Treeview",
                    rowheight=30,
                    font=('Arial', 14),
                    background="#f1f8e9",
                    foreground="#004d40",
                    fieldbackground="#f1f8e9",
                    bordercolor="#000000",
                    relief="solid",
                    borderwidth=1)
    style.configure("dash1.Treeview.Heading",
                    font=('Arial', 16, 'bold'),
                    background="#a5d6a7",
                    foreground="#004d40")
    style.map("dash1.Treeview",
              background=[('selected', '#c8e6c9')],
              foreground=[('selected', '#004d40')])

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=250, anchor="center")

    tree.pack(pady=10, fill="both", expand=True)

    scrollbar = ttk.Scrollbar(tree, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    xscrollbar = ttk.Scrollbar(tree, orient=tk.HORIZONTAL, command=tree.xview)
    tree.configure(xscroll=xscrollbar.set)
    xscrollbar.pack(side="bottom", fill="x")

    tree.pack(side="left", fill="both", expand=True)

    tree.bind("<Double-1>", lambda event: on_double_click(event, tree))

# Main function and other components of your application remain unchanged.
