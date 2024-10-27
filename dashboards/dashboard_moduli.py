import customtkinter as ctk
from tkinter import filedialog, Toplevel, Text, Scrollbar, messagebox
import pandas as pd
import os

def show_dashboard7(parent_frame):

    form_frame = ctk.CTkFrame(parent_frame, corner_radius=5)
    form_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Pulsante per caricare il file Excel
    upload_button = ctk.CTkButton(form_frame, text="Carica File Excel", command=upload_file, corner_radius=5)
    upload_button.grid(row=0, columnspan=2, pady=20)

    # Pulsante per mostrare i dati caricati in un pop-up
    show_data_button = ctk.CTkButton(form_frame, text="Mostra Dati", command=show_data_popup, corner_radius=5)
    show_data_button.grid(row=1, columnspan=2, pady=20)

def upload_file():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if file_path:
        if os.path.isfile(file_path) and file_path.endswith(('.xlsx', '.xls')):
            try:
                df = pd.read_excel(file_path)
                messagebox.showinfo("Successo", "File Excel caricato correttamente.")
            except Exception as e:
                messagebox.showerror("Errore", f"Errore durante il caricamento del file: {e}")
        else:
            messagebox.showerror("Errore", "Formato file non supportato. Carica un file Excel.")
    else:
        messagebox.showwarning("Avviso", "Nessun file selezionato.")

# Funzione per mostrare i dati in un pop-up
def show_data_popup():
    if df is None:
        messagebox.showerror("Errore", "Nessun file Excel caricato.")
        return

    popup = Toplevel()
    popup.title("Dati Excel")

    text_area = Text(popup, wrap='none', width=100, height=20)
    scrollbar_y = Scrollbar(popup, orient="vertical", command=text_area.yview)
    scrollbar_x = Scrollbar(popup, orient="horizontal", command=text_area.xview)

    text_area.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    text_area.grid(row=0, column=0, sticky='nsew')
    scrollbar_y.grid(row=0, column=1, sticky='ns')
    scrollbar_x.grid(row=1, column=0, sticky='ew')

    popup.grid_rowconfigure(0, weight=1)
    popup.grid_columnconfigure(0, weight=1)

    # Visualizza i dati come testo nel popup
    text_area.insert('1.0', df.to_string(index=False))

    popup.mainloop()
