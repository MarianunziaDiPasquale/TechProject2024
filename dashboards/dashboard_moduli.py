import customtkinter as ctk
from tkinter import filedialog, Tk, messagebox
from tkinter.ttk import Combobox
from tkinterdnd2 import TkinterDnD
import pandas as pd
import os

def show_dashboard7(parent_frame):

    form_frame = ctk.CTkFrame(parent_frame, corner_radius=5)
    form_frame.pack(pady=10, padx=10, fill="both", expand=True)

    label_fornitore = ctk.CTkLabel(form_frame, text="Fornitore:", font=('Arial', 14))
    label_fornitore.grid(row=0, column=0, padx=10, pady=10)
    combo_fornitore = Combobox(form_frame)
    combo_fornitore.grid(row=0, column=1, padx=10, pady=10)
    combo_fornitore.bind("<<ComboboxSelected>>", lambda event: update_data_combo(combo_fornitore, combo_data, combo_importo))

    label_data = ctk.CTkLabel(form_frame, text="Data:", font=('Arial', 14))
    label_data.grid(row=1, column=0, padx=10, pady=10)
    combo_data = Combobox(form_frame)
    combo_data.grid(row=1, column=1, padx=10, pady=10)

    label_importo = ctk.CTkLabel(form_frame, text="Importo:", font=('Arial', 14))
    label_importo.grid(row=2, column=0, padx=10, pady=10)
    combo_importo = Combobox(form_frame)
    combo_importo.grid(row=2, column=1, padx=10, pady=10)

    upload_button = ctk.CTkButton(form_frame, text="Carica File Excel", command=lambda: upload_file(combo_fornitore, combo_data, combo_importo), corner_radius=5)
    upload_button.grid(row=4, columnspan=2, pady=20)

def update_data_combo(combo_fornitore, combo_data, combo_importo):
    selected_fornitore = combo_fornitore.get()
    # Filtra i dati in base al fornitore selezionato
    filtered_df = df[df['Fornitore'] == selected_fornitore]
    combo_data['values'] = list(filtered_df['Data'])
    combo_data.current(0)
    update_importo_combo(combo_data, combo_importo)

def update_importo_combo(combo_data, combo_importo):
    selected_data = combo_data.get()
    # Filtra i dati in base alla data selezionata
    filtered_df = df[df['Data'] == selected_data]
    combo_importo['values'] = list(filtered_df['Importo'])
    combo_importo.current(0)

def upload_file(combo_fornitore, combo_data, combo_importo):
    global df
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if file_path:
        if os.path.isfile(file_path) and file_path.endswith(('.xlsx', '.xls')):
            try:
                df = pd.read_excel(file_path)
                # Assumi che il file Excel abbia colonne "Fornitore", "Data", "Importo"
                if 'Fornitore' in df.columns and 'Data' in df.columns and 'Importo' in df.columns:
                    # Popola il primo combobox con i fornitori
                    combo_fornitore['values'] = list(df['Fornitore'].unique())
                    combo_fornitore.current(0)
                    update_data_combo(combo_fornitore, combo_data, combo_importo)
                    messagebox.showinfo("Successo", "File Excel caricato correttamente.")
                else:
                    messagebox.showerror("Errore", "Il file Excel non contiene le colonne richieste.")
            except Exception as e:
                messagebox.showerror("Errore", f"Si è verificato un errore durante il caricamento del file: {e}")
        else:
            messagebox.showerror("Errore", "Formato di file non supportato. Per favore carica un file Excel.")
    else:
        messagebox.showwarning("Avviso", "Nessun file selezionato.")

def insert_invoice(combo_fornitore, combo_data, combo_importo):
    fornitore = combo_fornitore.get()
    data = combo_data.get()
    importo = combo_importo.get()
    # Logica per inserire la fattura nel database o gestire l'inserimento dei dati
    print(f"Fornitore: {fornitore}, Data: {data}, Importo: {importo}")
    # Puoi aggiungere qui il codice per salvare i dati nel database