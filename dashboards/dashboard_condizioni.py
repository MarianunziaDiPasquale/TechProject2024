import customtkinter as ctk
from tkinter import Toplevel, Listbox, Scrollbar, Entry, Button, Label, messagebox
import tkinter as tk
from Database_Utilities.crud_condizioni import (
    get_all_table1, add_table1_record, update_table1_record, delete_table1_record
)
from Database_Utilities.crud_metodi import (
    get_all_table2, add_table2_record, update_table2_record, delete_table2_record
)

dashboard_font_size = 14


def populate_listbox(listbox, data):
    """Populate the listbox with data."""
    listbox.delete(0, tk.END)
    for item in data:
        listbox.insert(tk.END, f"ID: {item['id']} - Nome: {item['nome']}")


def show_dashboard10(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    parent_frame_color = parent_frame.cget("fg_color")

    # Fetch data from the database
    table1_data = get_all_table1()
    table2_data = get_all_table2()

    # Crea due frame per contenere le liste
    frame_table1 = ctk.CTkFrame(parent_frame, corner_radius=5)
    frame_table1.pack(side="left", padx=5, pady=10, fill="both", expand=True)

    frame_table2 = ctk.CTkFrame(parent_frame, corner_radius=5)
    frame_table2.pack(side="right", padx=5, pady=10, fill="both", expand=True)

    # Etichette per le due tabelle
    label_table1 = ctk.CTkLabel(frame_table1, text="Condizioni pagamento", font=('Arial', dashboard_font_size))
    label_table1.pack(pady=5)

    label_table2 = ctk.CTkLabel(frame_table2, text="Metodi pagamento", font=('Arial', dashboard_font_size))
    label_table2.pack(pady=5)

    # Crea le liste di elementi
    listbox_table1 = Listbox(frame_table1, font=('Arial', dashboard_font_size), height=10)
    listbox_table2 = Listbox(frame_table2, font=('Arial', dashboard_font_size), height=10)

    # Aggiungi uno scrollbar per ogni lista
    scrollbar_table1 = Scrollbar(frame_table1, orient="vertical", command=listbox_table1.yview)
    scrollbar_table1.pack(side="right", fill="y")
    listbox_table1.configure(yscrollcommand=scrollbar_table1.set)
    listbox_table1.pack(fill="both", expand=True)

    scrollbar_table2 = Scrollbar(frame_table2, orient="vertical", command=listbox_table2.yview)
    scrollbar_table2.pack(side="right", fill="y")
    listbox_table2.configure(yscrollcommand=scrollbar_table2.set)
    listbox_table2.pack(fill="both", expand=True)

    # Populate the listboxes with data
    populate_listbox(listbox_table1, table1_data)
    populate_listbox(listbox_table2, table2_data)

    # Aggiungi il doppio clic per aprire il popup di modifica/eliminazione
    listbox_table1.bind("<Double-1>", lambda event: open_popup(listbox_table1, table1_data, update_table1_record, delete_table1_record))
    listbox_table2.bind("<Double-1>", lambda event: open_popup(listbox_table2, table2_data, update_table2_record, delete_table2_record))

    # Pulsanti per aggiungere nuovi elementi
    add_button_table1 = ctk.CTkButton(frame_table1, text="Aggiungi Elemento", font=("Arial", dashboard_font_size),
                                      command=lambda: open_add_popup("Tabella 1", table1_data, listbox_table1, add_table1_record))
    add_button_table1.pack(side="left", padx=10)

    add_button_table2 = ctk.CTkButton(frame_table2, text="Aggiungi Elemento", font=("Arial", dashboard_font_size),
                                      command=lambda: open_add_popup("Tabella 2", table2_data, listbox_table2, add_table2_record))
    add_button_table2.pack(side="left", padx=10)


def open_popup(listbox, data, update_func, delete_func):
    selected_item = listbox.curselection()
    if not selected_item:
        return

    index = selected_item[0]
    item = data[index]

    # Crea il popup
    popup = Toplevel()
    popup.title(f"Modifica/Elimina {item['nome']}")

    # Campi precompilati per ID e Nome
    label_id = Label(popup, text="ID:", font=('Arial', dashboard_font_size))
    label_id.pack(pady=5)
    entry_id = Entry(popup, font=('Arial', dashboard_font_size))
    entry_id.pack(pady=5)
    entry_id.insert(0, item['id'])

    label_nome = Label(popup, text="Nome:", font=('Arial', dashboard_font_size))
    label_nome.pack(pady=5)
    entry_nome = Entry(popup, font=('Arial', dashboard_font_size))
    entry_nome.pack(pady=5)
    entry_nome.insert(0, item['nome'])

    # Funzione per salvare le modifiche
    def save_changes():
        new_id = entry_id.get()
        new_nome = entry_nome.get()

        if new_id.isdigit():
            try:
                update_func(int(new_id), new_nome)  # Update in the database
                item["id"] = int(new_id)
                item["nome"] = new_nome
                populate_listbox(listbox, data)
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Errore", f"Errore durante l'aggiornamento: {e}")
        else:
            messagebox.showerror("Errore", "L'ID deve essere un numero!")

    # Funzione per eliminare l'elemento
    def delete_item():
        confirm = messagebox.askokcancel("Conferma", f"Sei sicuro di voler eliminare {item['nome']}?")
        if confirm:
            try:
                delete_func(item["id"])  # Delete from the database
                del data[index]
                populate_listbox(listbox, data)
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Errore", f"Errore durante l'eliminazione: {e}")

    # Pulsanti per salvare le modifiche o eliminare
    save_button = ctk.CTkButton(popup, text="Salva Modifiche", command=save_changes, font=('Arial', dashboard_font_size))
    save_button.pack(pady=10)

    delete_button = ctk.CTkButton(popup, text="Elimina Elemento", command=delete_item, font=('Arial', dashboard_font_size))
    delete_button.pack(pady=10)


def open_add_popup(tabella, data, listbox, add_func):
    popup = Toplevel()
    popup.title(f"Aggiungi Elemento a {tabella}")

    label_id = Label(popup, text="ID:", font=('Arial', dashboard_font_size))
    label_id.pack(pady=5)
    entry_id = Entry(popup, font=('Arial', dashboard_font_size))
    entry_id.pack(pady=5)

    label_nome = Label(popup, text="Nome:", font=('Arial', dashboard_font_size))
    label_nome.pack(pady=5)
    entry_nome = Entry(popup, font=('Arial', dashboard_font_size))
    entry_nome.pack(pady=5)

    # Funzione per salvare il nuovo elemento
    def add_new_item():
        new_id = entry_id.get()
        new_nome = entry_nome.get()

        if new_id.isdigit():
            try:
                add_func(int(new_id), new_nome)  # Add to the database
                new_item = {"id": int(new_id), "nome": new_nome}
                data.append(new_item)
                populate_listbox(listbox, data)
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Errore", f"Errore durante l'aggiunta: {e}")
        else:
            messagebox.showerror("Errore", "L'ID deve essere un numero!")

    add_button = ctk.CTkButton(popup, text="Aggiungi Elemento", command=add_new_item, font=('Arial', dashboard_font_size))
    add_button.pack(pady=10)
