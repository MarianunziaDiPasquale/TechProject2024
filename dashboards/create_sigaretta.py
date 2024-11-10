from tkinter import ttk, messagebox ,filedialog
import tkinter as tk
import customtkinter as ctk
import sqlite3
import os
import datetime
from datetime import datetime
from fpdf import FPDF
from PIL import Image, ImageTk
import fitz
from Database_Utilities.crud_clienti import get_all_clienti_names
import sqlite3

# Path to the SQLite database
db_path = 'Database_Utilities/Database/Magazzino.db'
class PDFSigarette(FPDF):
    def header_top(self, current_stringa):
        self.set_font('Arial', 'B', 14)
        current_date = datetime.now().strftime("%d/%m/%Y")
        self.cell(200, 10, txt=f"PAGAMENTO IN CONTANTI       Data: {current_date}", ln=True, align='C')
        # Aggiungi la data corrente nel formato GG/MM/AAAA
        # self.cell(200, 10, txt=f"Data: {current_date}", ln=True, align='C')
        self.cell(200, 10, txt=f"{current_stringa}", ln=True, align='C')

        # Spazio aggiuntivo dopo l'intestazione
        self.ln(10)

    '''
    def add_table_headers(self):
        self.set_font('Arial', 'B', 10)
        self.cell(20, 10, 'Codice', 1, align='C')
        self.cell(70, 10, 'Descrizione', 1, align='C')
        self.cell(20, 10, 'Quantità', 1, align='C')
        self.cell(20, 10, 'Prezzo', 1, align='C')
        self.cell(30, 10, 'Sconto/Magg.', 1, align='C')
        self.cell(20, 10, 'Importo', 1, align='C')
        self.ln()
    '''

    def add_table_row(self, codice, descrizione, quantita, prezzo, sconto, importo):
        self.set_font('Arial', '', 8)
        self.cell(20, 10, codice if codice else '', 0, align='C')
        self.cell(70, 10, descrizione if descrizione else '', 0, align='C')
        self.cell(20, 10, quantita if quantita else '', 0, align='C')
        self.cell(20, 10, prezzo if prezzo else '', 0, align='C')
        self.cell(30, 10, sconto if sconto else '', 0, align='C')
        self.cell(20, 10, importo if importo else '', 0, align='C')

    def add_extra_fields(self, esistenza, disponibilita, trasporto, imballo, varie, bollo, totale_merce,
                         totale_quantita, totale_fattura):
        self.set_font('Arial', '', 10)
        self.ln(20)
        self.cell(50, 10, f"{esistenza}", 0, 0, align='C')
        self.cell(50, 10, f"{disponibilita}", 0, 0, align='C')
        self.cell(50, 10, f"{trasporto}", 0, 1, align='C')
        self.cell(50, 10, f"{imballo}", 0, 0, align='C')
        self.cell(50, 10, f"{varie}", 0, 0, align='C')
        self.cell(50, 10, f"{bollo}", 0, 1, align='C')
        self.cell(50, 10, f"{totale_merce}", 0, 0, align='C')
        self.cell(50, 10, f"{totale_quantita}", 0, 0, align='C')
        self.cell(50, 10, f"{totale_fattura}", 0, 1, align='C')


def generate_pdf_sigaretta():
    # Popup window to edit and confirm invoice data
    def edit_and_confirm():
        def save_changes():
            # Salva i valori dei campi extra
            stringa = entry_stringa.get()
            esistenza = entry_esistenza.get()
            disponibilita = entry_disponibilita.get()
            trasporto = entry_trasporto.get()
            imballo = entry_imballo.get()
            varie = entry_varie.get()
            bollo = entry_bollo.get()
            # qui vanno sistemate queste quantità per calcolare il totale
            totale_merce = entry_bollo.get()
            totale_quantita = entry_totale_quantita.get()
            totale_fattura = entry_totale_fattura.get()

            # Recupera i dati dei prodotti
            products = []
            for row_entries in entries:
                codice = row_entries[0].get()
                descrizione = row_entries[1].get()
                quantita = row_entries[2].get()
                prezzo = row_entries[3].get()
                sconto = row_entries[4].get()
                importo = row_entries[5].get()
                if any([codice, descrizione, quantita, prezzo, sconto, importo]):
                    products.append([codice, descrizione, quantita, prezzo, sconto, importo])

            # Chiudi il popup e chiedi il percorso di salvataggio
            popup.destroy()
            choose_save_path(stringa, esistenza, disponibilita, trasporto, imballo, varie, bollo, totale_merce,
                             totale_quantita, totale_fattura, products)

        # Ottiene la data corrente e la formatta come YYYYMMDD
        current_date = datetime.now().strftime("%Y%m%d")
        filename = f"Fattura_Sigaretta_{current_date}"

        def choose_save_path(stringa, esistenza, disponibilita, trasporto, imballo, varie, bollo, totale_merce,
                             totale_quantita, totale_fattura, products):
            save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")],
                                                     initialfile=filename)
            if save_path:
                pdf = PDFSigarette()
                pdf.add_page()
                pdf.header_top(stringa)

                # Aggiungi le intestazioni della tabella e i prodotti
                # pdf.add_table_headers()
                for product in products:
                    pdf.add_table_row(*product)

                # Aggiungi i campi extra
                pdf.add_extra_fields(esistenza, disponibilita, trasporto, imballo, varie, bollo, totale_merce,
                                     totale_quantita, totale_fattura)

                # Salva il PDF
                pdf.output(save_path)
                messagebox.showinfo("Successo", f"PDF generato e salvato come {os.path.basename(save_path)}")
            else:
                messagebox.showwarning("Annullato", "Salvataggio PDF annullato")

        # Crea il popup per l'inserimento dei dati
        popup = tk.Toplevel()
        popup.title("Modifica i dati della fattura")
        popup.geometry("1800x700")

        padding = {'padx': 20, 'pady': 5}  # Spaziatura extra a sinistra per le entry
        # Set the width of entry fields and the font size
        entry_width = 20
        font_size = ("Arial", 14)  # Font family Arial, size 14

        # Entry per i prodotti
        entries = []
        headers = ["Codice", "Descrizione", "Quantità", "Prezzo", "Sconto/Magg.", "Importo"]
        for i, header in enumerate(headers):
            tk.Label(popup, text=header, font=font_size).grid(row=0, column=i + 1, **padding)

        for row in range(1, 11):  # Imposta 10 righe per inserimento prodotti
            row_entries = []
            clienti = get_all_clienti_names()
            condizione_selezionata = tk.StringVar()
            entry_article = ttk.Combobox(popup, textvariable=condizione_selezionata, values=clienti, font=font_size)
            entry_article.configure(width=25)
            entry_article.grid(row=row, column=1, padx=0, pady=0)
            entry_article.bind("<<ComboboxSelected>>", lambda event, r=row: update_row_description_and_price(r))
            row_entries.append(entry_article)

            entry_description = tk.Entry(popup, width=25, font=font_size)
            entry_description.grid(row=row, column=2, padx=0, pady=0)
            row_entries.append(entry_description)

            entry_quantity = tk.Entry(popup, width=entry_width, font=font_size)
            entry_quantity.grid(row=row, column=3, padx=0, pady=0)
            entry_quantity.bind("<KeyRelease>", lambda e: calculate_total_amount())
            row_entries.append(entry_quantity)

            # Prezzo (Entry)
            entry_price = tk.Entry(popup, width=entry_width, font=font_size)
            entry_price.grid(row=row, column=4, padx=0, pady=0)
            entry_price.bind("<KeyRelease>", lambda e: calculate_total_amount())
            row_entries.append(entry_price)

            # Sconto/Magg. (Entry)
            entry_discount = tk.Entry(popup, width=entry_width, font=font_size)
            entry_discount.grid(row=row, column=5, padx=0, pady=0)
            entry_discount.bind("<KeyRelease>", lambda e: calculate_total_amount())
            row_entries.append(entry_discount)

            # Importo (Entry)
            entry_amount = tk.Entry(popup, width=entry_width, font=font_size)
            entry_amount.grid(row=row, column=6, padx=0, pady=0)
            row_entries.append(entry_amount)

            entries.append(row_entries)
        '''
            for col in range(6):  # 6 colonne (Codice, Descrizione, ecc.)
                entry = tk.Entry(popup, width=entry_width, font=font_size)
                entry.grid(row=row, column=col + 1, padx=0, pady=0)
                row_entries.append(entry)
            entries.append(row_entries)

        for row_entries in entries:
            row_entries[2].bind("<KeyRelease>", lambda e: calculate_totals())  # Quantity column
            row_entries[3].bind("<KeyRelease>", lambda e: calculate_totals())

        '''

        def update_row_description_and_price(row):
            """Update description and price for a given row based on the selected article"""
            entry_article = entries[row - 1][0]  # Combobox for Codice
            entry_description = entries[row - 1][1]  # Entry for Descrizione
            entry_price = entries[row - 1][3]  # Entry for Prezzo

            article = entry_article.get()
            description = fetch_description_for_article(article)
            entry_description.delete(0, tk.END)
            entry_description.insert(0, description)

            price = fetch_price_for_article(article)
            entry_price.delete(0, tk.END)
            entry_price.insert(0, price)

        def fetch_description_for_article(article):
            """Fetches the description (Indirizzo) for the selected article from the database."""
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT `Indirizzo` FROM clienti WHERE `Ragione Sociale` = ?;", (article,))
            result = cursor.fetchone()
            conn.close()
            description = result[0] if result else ""
            return description

        def fetch_price_for_article(article):
            """Fetches the price (CAP) for the selected article from the database."""
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT `CAP` FROM clienti WHERE `Ragione Sociale` = ?;", (article,))
            result = cursor.fetchone()
            conn.close()
            price = result[0] if result else ""
            return price

        # Aggiungi una riga di spazio tra i prodotti e gli altri campi
        spacer = tk.Label(popup, text="", font=font_size)
        spacer.grid(row=11, columnspan=7, pady=10)

        # Entry per i campi extra (con spaziatura a sinistra)
        tk.Label(popup, text="Esistenza", font=font_size).grid(row=12, column=0, padx=20, pady=5)
        entry_esistenza = tk.Entry(popup, width=entry_width, font=font_size)
        entry_esistenza.grid(row=12, column=1)

        tk.Label(popup, text="Disponibilità", font=font_size).grid(row=13, column=0, padx=20, pady=5)
        entry_disponibilita = tk.Entry(popup, width=entry_width, font=font_size)
        entry_disponibilita.grid(row=13, column=1)

        tk.Label(popup, text="Trasporto", font=font_size).grid(row=12, column=2, padx=20, pady=5)
        entry_trasporto = tk.Entry(popup, width=entry_width, font=font_size)
        entry_trasporto.grid(row=12, column=3)

        tk.Label(popup, text="Imballo", font=font_size).grid(row=13, column=2, padx=20, pady=5)
        entry_imballo = tk.Entry(popup, width=entry_width, font=font_size)
        entry_imballo.grid(row=13, column=3)

        tk.Label(popup, text="Varie", font=font_size).grid(row=12, column=4, padx=20, pady=5)
        entry_varie = tk.Entry(popup, width=entry_width, font=font_size)
        entry_varie.grid(row=12, column=5)

        tk.Label(popup, text="Bollo", font=font_size).grid(row=13, column=4, padx=20, pady=5)
        entry_bollo = tk.Entry(popup, width=entry_width, font=font_size)
        entry_bollo.grid(row=13, column=5)
        entry_bollo.bind("<KeyRelease>", lambda e: calculate_total_amount())

        tk.Label(popup, text="Fornitore", font=font_size).grid(row=14, column=4, padx=20, pady=5)
        entry_stringa = tk.Entry(popup, width=entry_width, font=font_size)
        entry_stringa.grid(row=14, column=5)

        def calculate_total_amount():
            total_quantity = 0
            total_merce = 0.0
            # Iterate through each row to calculate total amount with discount applied
            for row_entries in entries:
                try:
                    # Fetch values from the entries in each row
                    quantity = float(row_entries[2].get() or 0)  # Quantity is in column 3
                    price = float(row_entries[3].get() or 0)  # Price is in column 4
                    discount = float(row_entries[4].get() or 0) / 100  # Discount is in column 5

                    # Calculate total for the row as (quantity * price) - discount
                    row_total = (quantity * price) - (quantity * price * discount)

                    # Update Totale Quantità and Totale Merce
                    total_quantity += quantity
                    total_merce += row_total

                    # Update Importo (total amount) for the current row
                    row_entries[5].config(state='normal')
                    row_entries[5].delete(0, tk.END)
                    row_entries[5].insert(0, f"{row_total:.2f}")
                    row_entries[5].config(state='readonly')

                except ValueError:
                    # Ignore rows with invalid or empty entries
                    pass

            # Calculate Totale Fattura as Totale Merce plus Bollo
            try:
                bollo = float(entry_bollo.get() or 0)
            except ValueError:
                bollo = 0

            total_fattura = total_merce + bollo

            # Update the UI with calculated totals
            entry_totale_quantita.config(state='normal')
            entry_totale_quantita.delete(0, tk.END)
            entry_totale_quantita.insert(0, f"{total_quantity:.2f}")
            entry_totale_quantita.config(state='readonly')

            entry_totale_merce.config(state='normal')
            entry_totale_merce.delete(0, tk.END)
            entry_totale_merce.insert(0, f"{total_merce:.2f}")
            entry_totale_merce.config(state='readonly')

            entry_totale_fattura.config(state='normal')
            entry_totale_fattura.delete(0, tk.END)
            entry_totale_fattura.insert(0, f"{total_fattura:.2f}")
            entry_totale_fattura.config(state='readonly')

        tk.Label(popup, text="Totale Merce", font=font_size).grid(row=14, column=4, padx=20, pady=5)
        entry_totale_merce = tk.Entry(popup, width=entry_width, font=font_size)
        entry_totale_merce.grid(row=14, column=5)

        tk.Label(popup, text="Totale Quantità", font=font_size).grid(row=14, column=2, padx=20, pady=5)
        entry_totale_quantita = tk.Entry(popup, width=entry_width, font=font_size)
        entry_totale_quantita.grid(row=14, column=3)

        tk.Label(popup, text="Totale Fattura", font=font_size).grid(row=14, column=0, padx=20, pady=5)
        entry_totale_fattura = tk.Entry(popup, width=entry_width, font=font_size)
        entry_totale_fattura.grid(row=14, column=1)

        # Bottone per confermare e salvare
        tk.Button(popup, text="Salva e Genera PDF", font=font_size, command=save_changes).grid(row=15, columnspan=6,
                                                                                               pady=20)

        # Richiama la funzione di editing e conferma

    edit_and_confirm()