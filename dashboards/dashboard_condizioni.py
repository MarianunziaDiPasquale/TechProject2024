import customtkinter as ctk
from tkinter import Toplevel, Listbox, Scrollbar, Entry, Button, Label, messagebox
import tkinter as tk

# Simuliamo le due tabelle con delle liste (puoi sostituire con le tue query al database)
table1_data = [{"id": 1, "nome": "Prelevement le 17 mois suivant"}, {"id": 2, "nome": "Prelevement le 20 mois suivant"}]
table2_data = [{"id": 1, "nome": "MP20 SEPA Direct Debit CORE"}, {"id": 2, "nome": "MP05"}]


# Funzione per mostrare la dashboard con le due liste
def show_dashboard10(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Crea due frame per contenere le liste
    frame_table1 = ctk.CTkFrame(parent_frame, corner_radius=5)
    frame_table1.pack(side="left", padx=5, pady=10, fill="both", expand=True)

    frame_table2 = ctk.CTkFrame(parent_frame, corner_radius=5)
    frame_table2.pack(side="right", padx=5, pady=10, fill="both", expand=True)

    # Etichette per le due tabelle
    label_table1 = ctk.CTkLabel(frame_table1, text="Condizioni pagamento", font=('Arial', 14))
    label_table1.pack(pady=5)

    label_table2 = ctk.CTkLabel(frame_table2, text="Metodi pagamento", font=('Arial', 14))
    label_table2.pack(pady=5)

    # Crea le liste di elementi
    listbox_table1 = Listbox(frame_table1, font=('Arial', 14), height=10)
    listbox_table2 = Listbox(frame_table2, font=('Arial', 14), height=10)

    # Aggiungi uno scrollbar per ogni lista
    scrollbar_table1 = Scrollbar(frame_table1, orient="vertical", command=listbox_table1.yview)
    scrollbar_table1.pack(side="right", fill="y")
    listbox_table1.configure(yscrollcommand=scrollbar_table1.set)
    listbox_table1.pack(fill="both", expand=True)

    scrollbar_table2 = Scrollbar(frame_table2, orient="vertical", command=listbox_table2.yview)
    scrollbar_table2.pack(side="right", fill="y")
    listbox_table2.configure(yscrollcommand=scrollbar_table2.set)
    listbox_table2.pack(fill="both", expand=True)

    # Popola le liste con gli elementi
    for item in table1_data:
        listbox_table1.insert(tk.END, f"ID: {item['id']} - Nome: {item['nome']}")

    for item in table2_data:
        listbox_table2.insert(tk.END, f"ID: {item['id']} - Nome: {item['nome']}")

    # Aggiungi il doppio clic per aprire il popup di modifica/eliminazione
    listbox_table1.bind("<Double-1>", lambda event: open_popup(listbox_table1, table1_data))
    listbox_table2.bind("<Double-1>", lambda event: open_popup(listbox_table2, table2_data))

    # Pulsanti per aggiungere nuovi elementi
    add_button_table1 = ctk.CTkButton(frame_table1, text="Aggiungi Elemento",
                                      command=lambda: open_add_popup("Tabella 1", table1_data, listbox_table1))
    add_button_table1.pack(pady=10)

    add_button_table2 = ctk.CTkButton(frame_table2, text="Aggiungi Elemento",
                                      command=lambda: open_add_popup("Tabella 2", table2_data, listbox_table2))
    add_button_table2.pack(pady=10)


# Funzione per aprire il popup di modifica/eliminazione
def open_popup(listbox, data):
    selected_item = listbox.curselection()
    if not selected_item:
        return

    index = selected_item[0]
    item = data[index]

    # Crea il popup
    popup = Toplevel()
    popup.title(f"Modifica/Elimina {item['nome']}")

    # Campi precompilati per ID e Nome
    label_id = Label(popup, text="ID:", font=('Arial', 14))
    label_id.pack(pady=5)
    entry_id = Entry(popup, font=('Arial', 14))
    entry_id.pack(pady=5)
    entry_id.insert(0, item['id'])

    label_nome = Label(popup, text="Nome:", font=('Arial', 14))
    label_nome.pack(pady=5)
    entry_nome = Entry(popup, font=('Arial', 14))
    entry_nome.pack(pady=5)
    entry_nome.insert(0, item['nome'])

    # Funzione per salvare le modifiche
    def save_changes():
        new_id = entry_id.get()
        new_nome = entry_nome.get()

        if new_id.isdigit():
            item['id'] = int(new_id)
            item['nome'] = new_nome
            listbox.delete(index)
            listbox.insert(index, f"ID: {item['id']} - Nome: {item['nome']}")
            popup.destroy()
        else:
            messagebox.showerror("Errore", "L'ID deve essere un numero!")

    # Funzione per eliminare l'elemento
    def delete_item():
        confirm = messagebox.askokcancel("Conferma", f"Sei sicuro di voler eliminare {item['nome']}?")
        if confirm:
            del data[index]
            listbox.delete(index)
            popup.destroy()

    # Pulsanti per salvare le modifiche o eliminare
    save_button =ctk.CTkButton(popup, text="Salva Modifiche", command=save_changes, width=120, height=30)
    save_button.pack(pady=10)

    delete_button = ctk.CtkButton(popup, text="Elimina Elemento", command=delete_item, width=120, height=30)
    delete_button.pack(pady=10)


# Funzione per aggiungere un nuovo elemento
def open_add_popup(tabella, data, listbox):
    popup = Toplevel()
    popup.title(f"Aggiungi Elemento a {tabella}")

    label_id = Label(popup, text="ID:", font=('Arial', 14))
    label_id.pack(pady=5)
    entry_id = Entry(popup, font=('Arial', 14))
    entry_id.pack(pady=5)

    label_nome = Label(popup, text="Nome:", font=('Arial', 14))
    label_nome.pack(pady=5)
    entry_nome = Entry(popup, font=('Arial', 14))
    entry_nome.pack(pady=5)

    # Funzione per salvare il nuovo elemento
    def add_new_item():
        new_id = entry_id.get()
        new_nome = entry_nome.get()

        if new_id.isdigit():
            new_item = {"id": int(new_id), "nome": new_nome}
            data.append(new_item)
            listbox.insert(tk.END, f"ID: {new_item['id']} - Nome: {new_item['nome']}")
            popup.destroy()
        else:
            messagebox.showerror("Errore", "L'ID deve essere un numero!")

    add_button = ctk.CtkButton(popup, text="Aggiungi Elemento", command=add_new_item, width=120, height=30)
    add_button.pack(pady=10)

