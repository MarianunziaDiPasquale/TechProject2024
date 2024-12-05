from tkinter import ttk, messagebox, filedialog
import tkinter as tk
import customtkinter as ctk
import os
import datetime
from datetime import datetime
from fpdf import FPDF
from PIL import Image, ImageTk
import fitz
from Database_Utilities.crud_clienti import get_all_clienti_names
from Database_Utilities.connection import _connection



class PDFProvvigioni(FPDF):
    def header_top(self, agente):
        self.set_font('Arial', 'B', 14)
        current_date = datetime.now().strftime("%d/%m/%Y")
        self.cell(200, 10, txt=f"PAGAMENTO PROVVIGIONE      Data: {current_date}", ln=True, align='C')
        # Aggiungi la data corrente nel formato GG/MM/AAAA
        # self.cell(200, 10, txt=f"Data: {current_date}", ln=True, align='C')
        self.cell(200, 10, txt=f"{agente}", ln=True, align='C')

        # Spazio aggiuntivo dopo l'intestazione
        self.ln(10)

    def add_extra_fields(self, start_date, end_date, provvigione, totale_fattura):
        headers = ["Data Inizio", "Data Fine", "Provvigione", "Totale"]
        # Imposta il font per gli header
        self.set_font('Arial', 'B', 10)  # Grassetto per gli header
        self.ln(5)  # Spazio prima degli header

        # Stampa gli header
        for header in headers:
            self.cell(50, 10, header, 0, 0, align='L')  # Bordo=1 per le celle
        self.ln(5)  # Nuova riga dopo gli header

        self.set_font('Arial', '', 10)
        self.cell(50, 10, f"{start_date}", 0, 0, align='L')
        self.cell(50, 10, f"{end_date}", 0, 0, align='L')
        self.cell(50, 10, f"{provvigione}", 0, 0, align='L')
        self.cell(50, 10, f"{totale_fattura}", 0, 0, align='L')


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


def generate_pdf_provvigione(values, selected_fornitori):
    values_1 = list(values)
    print(values_1)
    print(selected_fornitori)

    def edit_and_confirm():
        def save_changes():
            # Salva i valori dei campi extra
            values_1[0] = entry_agente.get()
            values_1[1] = entry_provvigione.get()
            values_1[2] = entry_start_date.get()
            values_1[3] = entry_end_date.get()
            totale_fattura = entry_totale_fattura.get()

            # Chiudi il popup e chiedi il percorso di salvataggio
            popup.destroy()
            choose_save_path(values[0], values[1], values[2], values[3], totale_fattura)

        # Ottiene la data corrente e la formatta come YYYYMMDD
        current_date = datetime.now().strftime("%Y%m%d")
        filename = f"Fattura_Provvigione_{current_date}"

        def choose_save_path(agente_selezionato, provvigione, start_date, end_date, totale_fattura):
            save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")],
                                                     initialfile=filename)
            if save_path:
                pdf = PDFProvvigioni()
                pdf.add_page()
                pdf.header_top(agente_selezionato)

                # Aggiungi le intestazioni della tabella e i prodotti
                # pdf.add_table_headers()
                print("Prodotti nel PDF:")

                # Aggiungi i campi extra
                pdf.add_extra_fields(start_date, end_date, provvigione, totale_fattura)

                # Salva il PDF
                pdf.output(save_path)
                messagebox.showinfo("Successo", f"PDF generato e salvato come {os.path.basename(save_path)}")
            else:
                messagebox.showwarning("Annullato", "Salvataggio PDF annullato")

        # Crea il popup per l'inserimento dei dati
        popup = tk.Toplevel()
        popup.title("Modifica i dati della fattura provvigione")
        popup.geometry("1200x300")

        padding = {'padx': 20, 'pady': 5}  # Spaziatura extra a sinistra per le entry
        # Set the width of entry fields and the font size
        entry_width = 20
        font_size = ("Arial", 14)  # Font family Arial, size 14

        def fetch_description_for_article(article):
            """Fetches the description (Indirizzo) for the selected article from the database."""
            conn = _connection()
            cursor = conn.cursor()
            cursor.execute("SELECT `Indirizzo` FROM clienti WHERE `Ragione Sociale` = %s;", (article,))
            result = cursor.fetchone()
            conn.close()
            description = result[0] if result else ""
            return description

        def fetch_price_for_article(article):
            """Fetches the price (CAP) for the selected article from the database."""
            conn = _connection()
            cursor = conn.cursor()
            cursor.execute("SELECT `Indirizzo` FROM clienti WHERE `Ragione Sociale` = %s;", (article,))
            result = cursor.fetchone()
            conn.close()
            price = result[0] if result else ""
            return price

        tk.Label(popup, text="Agente selezionato", font=font_size).grid(row=1, column=0, padx=20, pady=5)
        entry_agente = tk.Entry(popup, width=entry_width, font=font_size)
        entry_agente.grid(row=1, column=2)
        entry_agente.insert(0, values[0])

        tk.Label(popup, text="Provvigione", font=font_size).grid(row=2, column=0, padx=20, pady=5)
        entry_provvigione = tk.Entry(popup, width=entry_width, font=font_size)
        entry_provvigione.grid(row=2, column=2)
        entry_provvigione.insert(0, values[1])
        #entry_provvigione.bind("<KeyRelease>", lambda e: calculate_total_amount())

        tk.Label(popup, text="Start date", font=font_size).grid(row=3, column=0, padx=20, pady=5)
        entry_start_date = tk.Entry(popup, width=entry_width, font=font_size)
        entry_start_date.grid(row=3, column=2)
        entry_start_date.insert(0, values[2])
        #entry_imballo.bind("<KeyRelease>", lambda e: calculate_total_amount())

        tk.Label(popup, text="End date", font=font_size).grid(row=4, column=0, padx=20, pady=5)
        entry_end_date = tk.Entry(popup, width=entry_width, font=font_size)
        entry_end_date.grid(row=4, column=2)
        entry_end_date.insert(0, values[3])
        #entry_varie.bind("<KeyRelease>", lambda e: calculate_total_amount())

        tk.Label(popup, text="Totale Fattura", font=font_size).grid(row=5, column=0, padx=20, pady=5)
        entry_totale_fattura = tk.Entry(popup, width=entry_width, font=font_size)
        entry_totale_fattura.grid(row=5, column=2)

        totale_fattura = 0

        try:
            # Converti le date da stringa a oggetti datetime
            start_date_obj = datetime.strptime(entry_start_date.get(), "%d/%m/%y")
            end_date_obj = datetime.strptime(entry_end_date.get(), "%d/%m/%y")

            # Calcola il numero di giorni tra le date
            num_days = (end_date_obj - start_date_obj).days
            print(num_days)

            # Calcola il totale basato sui fornitori selezionati
            for fornitore in selected_fornitori:
                lung_totale_fattura = 0
                lung_totale_fattura += len(fornitore)
                print(lung_totale_fattura)
                totale_fattura += len(fornitore) * num_days

        except ValueError as e:
            # Gestisci eventuali errori nel formato delle date
            messagebox.showerror("Errore", f"Formato data non valido: {e}")
            return

            # Inserisci il totale calcolato nell' entry corrispondente
        entry_totale_fattura.delete(0, tk.END)
        entry_totale_fattura.insert(0, str(totale_fattura))

        # Bottone per confermare e salvare
        ctk.CTkButton(popup, text="Salva e Genera PDF", font=font_size, command=save_changes).grid(row=15, column=1,
                                                                                                   pady=20)

        # Add save changes button at the bottom

        # Richiama la funzione di editing e conferma

    edit_and_confirm()
