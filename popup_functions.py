import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from data_retrieval import get_existing_names, delete_records_by_name, create_record_clienti, create_fornitore, create_record_prodotti
from Database_Utilities.crud_fornitori import get_all_fornitori
from Database_Utilities.crud_clienti import get_all_clienti_names
def open_remove_popup(item_type):
    popup = tk.Toplevel()
    popup.title(f"Rimuovi {item_type}")

    # Center the popup
    window_width = 400
    window_height = 200
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    popup.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    label = tk.Label(popup, text=f"Seleziona un {item_type} da rimuovere", font=('Arial', 14))
    label.pack(pady=10)

    names = get_existing_names(item_type)  # Get existing names for the specified item type

    selected_name = tk.StringVar()

    # Create Combobox with specified font
    style = ttk.Style()
    style.configure("TCombobox", font=('Arial', 14))  # Adjust font size as needed
    style.configure("TCombobox*Listbox*Font", font=('Arial', 14))  # Ensure larger font size for dropdown menu items

    combobox = ttk.Combobox(popup, textvariable=selected_name, values=names, font=('Arial', 14))
    combobox.pack(pady=10)

    # Create a style for the Listbox within the Combobox dropdown
    combobox.option_add('*TCombobox*Listbox*Font', ('Arial', 14))

    def on_confirm():
        selected = selected_name.get()
        if selected:
            delete_records_by_name(item_type, selected)
            print(f"Rimuovi - Selezionato {item_type}: {selected}")
        popup.destroy()

    confirm_button = tk.Button(popup, text="Conferma", command=on_confirm, font=('Arial', 12))
    confirm_button.pack(pady=10)

def open_add_popup(item_type):
    popup = tk.Toplevel()
    popup.title(f"Aggiungi {item_type}")

    # Center the popup
    window_width = 800
    window_height = 600

    label = tk.Label(popup, text=f"Inserisci i dettagli del nuovo {item_type}", font=('Arial', 14))
    label.pack(pady=10)

    entry_width = 40
    font_size = ("Arial", 14)  # Font family Arial, size 14

    entries = {}

    if item_type == "Cliente":
        window_width = 1300
        fields = ["Ragione Sociale", "2° riga rag. sociale", "Indirizzo", "CAP", "Città", "Nazione", "Partita IVA","Esente IVA", "Telefono", "Email", "Zona", "Giorni di chiusura", "Orari di scarico", "Condizioni di pagamento", "Sconto", "Agente 1", "ID Cliente"]
        form_frame = tk.Frame(popup)
        form_frame.pack(pady=10)

        for i, field in enumerate(fields):
            label = tk.Label(form_frame, text=field, font=font_size)
            label.grid(row=i//2, column=(i%2)*2, padx=5, pady=5, sticky='e')
            if field == "Condizioni di pagamento":
                clienti = get_all_clienti_names()  # Da modificare
                condizione_selezionata = tk.StringVar()
                condizione = ttk.Combobox(form_frame, textvariable=condizione_selezionata, values=clienti,
                                          font=("Arial", 14))
                condizione.configure(width=40)
                condizione.option_add('*TCombobox*Listbox*Font', ('Arial', 16))
                condizione.grid(row=i//2, column=(i%2)*2+1, padx=5, pady=5, sticky='w')
                entries[field] = condizione_selezionata
            elif field == "Esente IVA":
                esenzioni = ["si", "no"]  # Da modificare
                esente_selezionata = tk.StringVar()
                esenzione = ttk.Combobox(form_frame, textvariable=esente_selezionata, values=esenzioni,
                                         font=("Arial", 14))
                esenzione.configure(width=40)
                esenzione.option_add('*TCombobox*Listbox*Font', ('Arial', 16))
                esenzione.grid(row=i//2, column=(i%2)*2+1, padx=5, pady=5, sticky='w')
                entries[field] = esente_selezionata
            elif field == "Agente 1":
                agenti = get_all_clienti_names()  # Da modificare
                agente_selezionato = tk.StringVar()
                agente = ttk.Combobox(form_frame, textvariable=agente_selezionato, values=agenti,
                                      font=("Arial", 14))
                agente.configure(width=40)
                agente.option_add('*TCombobox*Listbox*Font', ('Arial', 16))
                agente.grid(row=i//2, column=(i%2)*2+1, padx=5, pady=5, sticky='w')
                entries[field] = agente_selezionato
            else:
                entry = tk.Entry(form_frame, width=entry_width, font=font_size)
                entry.grid(row=i//2, column=(i%2)*2+1, padx=5, pady=5, sticky='w')
                entries[field] = entry

    elif item_type == "Fornitore":
        fields = ["Nome", "ID Fornitore"]
        for field in fields:
            label = tk.Label(popup, text=field,width=entry_width, font=font_size)
            label.pack(pady=5)
            entry = tk.Entry(popup, font=font_size)
            entry.pack(pady=5)
            entries[field] = entry
    elif item_type == "Prodotto":
        fields = ["Codice", "Descrizione", "Fornitore", "Composizione Cartone", "Prezzo Vendita", "Prezzo Acquisto"]
        for field in fields:
            if field == "Fornitore":
                label = tk.Label(popup, text="Fornitore",width=entry_width, font=font_size)
                label.pack(pady=5)
                fornitori = get_all_fornitori() # Da modificare
                selected_fornitore = tk.StringVar()
                combobox = ttk.Combobox(popup, textvariable=selected_fornitore, values=fornitori,
                                        font=('Arial', 16))
                combobox.configure(width=25)
                combobox.option_add('*TCombobox*Listbox*Font', ('Arial', 16))
                combobox.pack(pady=5)
                entries[field] = combobox
            else:
                label = tk.Label(popup, text=field, width=entry_width, font=font_size)
                label.pack(pady=5)
                entry = tk.Entry(popup, font=font_size)
                entry.pack(pady=5)
                entries[field] = entry
    elif item_type == "Lista":
        fields = ["Prodotto"]
        for field in fields:
            if field == "Prodotto":
                label = tk.Label(popup, text="Prodotto",width=entry_width, font=font_size)
                label.pack(pady=5)
                clienti = get_all_clienti_names() # Da modificare
                selected_cliente = tk.StringVar()
                combobox = ttk.Combobox(popup, textvariable=selected_cliente, values=clienti,
                                        font=('Arial', 16))
                combobox.configure(width=35)
                combobox.option_add('*TCombobox*Listbox*Font', ('Arial', 16))
                combobox.pack(pady=5)
            else:
                label = tk.Label(popup, text=field, width=entry_width, font=font_size)
                label.pack(pady=5)
                entry = tk.Entry(popup, font=font_size)
                entry.pack(pady=5)
                entries[field] = entry
    elif item_type == "Vettore":
        fields = ["Nome", "ID Vettore"]
        for field in fields:
            label = tk.Label(popup, text=field,width=entry_width, font=font_size)
            label.pack(pady=5)
            entry = tk.Entry(popup, font=font_size)
            entry.pack(pady=5)
            entries[field] = entry
    elif item_type == "Agente":
        fields = ["Nome", "ID Agente"]
        for field in fields:
            label = tk.Label(popup, text=field,width=entry_width, font=font_size)
            label.pack(pady=5)
            entry = tk.Entry(popup, font=font_size)
            entry.pack(pady=5)
            entries[field] = entry
    elif item_type == "Cliente Connesso":
        fields = ["Agente", "ID", "Cliente Connesso"]
        for field in fields:
            label = tk.Label(popup, text=field,width=entry_width, font=font_size)
            label.pack(pady=5)
            entry = tk.Entry(popup, font=font_size)
            entry.pack(pady=5)
            entries[field] = entry
    elif item_type == "Provvigioni":
        fields = [ "Agente", "Provvigione"]
        form_frame = tk.Frame(popup)
        form_frame.pack(pady=10)
        for i, field in enumerate(fields):
            label = tk.Label(form_frame, text=field, font=font_size)
            label.grid(row=i // 2, column=(i % 2) * 2, padx=5, pady=5, sticky='e')
            if field == "Agente":
                clienti = get_all_clienti_names()  # Da modificare
                Agente_selezionata = tk.StringVar()
                Agente = ttk.Combobox(form_frame, textvariable=Agente_selezionata, values=clienti,
                                          font=("Arial", 14))
                Agente.configure(width=30)
                Agente.option_add('*TCombobox*Listbox*Font', ('Arial', 16))
                Agente.grid(row=i // 2, column=(i % 2) * 2 + 1, padx=5, pady=5, sticky='w')
                entries[field] = Agente_selezionata
            else:
                entry = tk.Entry(form_frame, width=entry_width, font=font_size)
                entry.grid(row=i // 2, column=(i % 2) * 2 + 1, padx=5, pady=5, sticky='w')
                entries[field] = entry




    def on_confirm():
        values = [entry.get() for entry in entries.values()]
        if item_type == "Cliente":
            create_record_clienti(*values)
        elif item_type == "Fornitore":
            create_fornitore(*values)
        elif item_type == "Prodotto":
            create_record_prodotti(*values)
        elif item_type == "Lista":
            #aggiungi per lista
            print("hello")
        elif item_type == "Vettore":
            #aggiungi per vettore
            print("hello")
        elif item_type == "Agente":
            #aggiunti per agente
            print("hello")
        elif item_type == "Cliente Connesso":
            #aggiungi per cliente connesso
            print("hello")
        elif item_type == "Provvigione":
            #aggiungi per cliente connesso
            print("hello")
        print(f"Aggiungi - Selezionato {item_type}: {values}")
        popup.destroy()


    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    popup.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
    confirm_button = tk.Button(popup, text="Conferma", command=on_confirm, font=('Arial', 12))
    confirm_button.pack(pady=10)