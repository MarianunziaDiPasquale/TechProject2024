from tkinter import ttk, messagebox ,filedialog
import tkinter as tk
import customtkinter as ctk
from Database_Utilities.connection import _connection
import os
import datetime
from datetime import datetime
from fpdf import FPDF
from PIL import Image, ImageTk
import fitz

def show_pdf_preview(pdf_path):
    # Apri il PDF con PyMuPDF
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)  # Carica la prima pagina

    window = tk.Toplevel()
    window.title("Anteprima del Documento PDF")

    # Conversione della pagina PDF in un'immagine TKinter
    zoom = 1  # Livello di zoom iniziale
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    photo = ImageTk.PhotoImage(image=img)
    label_image = tk.Label(window, image=photo)
    label_image.image = photo  # Mantieni una riferimento!
    label_image.pack()

    # Slider per controllare lo zoom
    def update_zoom(event=None):
        nonlocal photo, label_image
        zoom_factor = scale_zoom.get()
        mat = fitz.Matrix(zoom_factor, zoom_factor)
        pix = page.get_pixmap(matrix=mat)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        photo = ImageTk.PhotoImage(image=img)
        label_image.configure(image=photo)
        label_image.image = photo  # Aggiorna il riferimento

    scale_zoom = tk.Scale(window, from_=0.5, to=5.0, resolution=0.1, orient="horizontal", command=update_zoom)
    scale_zoom.set(zoom)  # Imposta lo zoom iniziale
    scale_zoom.pack(fill="x")

    window.mainloop()

def fetch_invoice_data(invoice_number):
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM `orders_fattura_newfields` WHERE `id` = %s", (invoice_number,))
    column_names = [description[0] for description in cursor.description]
    invoice_tuple = cursor.fetchone()
    conn.close()
    if invoice_tuple:
        invoice = dict(zip(column_names, invoice_tuple))
        return invoice
    return None


def fetch_invoice_products(invoice_number):
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT `article`, `product_description`, `product_quantity`, `product_price`, `product_discount`, `product_discount_2`, `product_discount_3`, `product_amount` FROM `orders_fattura_newfields` WHERE `id` = %s",
        (invoice_number,)
    )
    column_names = [description[0] for description in cursor.description]
    product_rows = cursor.fetchall()
    conn.close()
    products = [dict(zip(column_names, product_row)) for product_row in product_rows]
    return products


def format_field(value):
    """Ritorna il valore se non vuoto, altrimenti un trattino."""
    return value if value.strip() else "-"
class PDFNonSold(FPDF):
    def header(self):

        # Aggiungi il logo in alto a sinistra
        self.image("resources/LogoCINCOTTI.jpg", 8, 2, 77, 44,
                   'JPG')  # Modifica il percorso e le dimensioni

        # Aggiungi l'immagine in alto a destra
        self.image("resources/Logojpeg.jpg", 120, 8, 77, 33,
                   'JPG')  # Modifica il percorso e le dimensioni

        self.ln(35)

    def add_footer_on_last_page(self):
        # Verifica di essere sull'ultima pagina, non occorre usare alias_nb_pages
        self.set_y(-40)  # Posiziona a 40 mm dal fondo della pagina
        self.image("resources/LOGOMOZZABELLAECINCOTTI.jpg", 75, self.get_y(), 70, 40, 'JPG')

    def draw_table(self, data, col_widths, headers=None, bold_headers=False):
        # Memorizza la posizione corrente della coordinata Y
        start_y = self.get_y()
        print(start_y, "start table")

        # Calcola l'altezza della tabella
        table_height = self.calculate_table_height(data, col_widths, headers)
        '''

        # Verifica se c'è abbastanza spazio sulla pagina corrente, altrimenti aggiungi una nuova pagina
        if start_y + table_height > self.page_break_trigger:
            self.add_page()
            start_y = self.get_y()  # Aggiorna la posizione di inizio sulla nuova pagina
        '''

        # Stampa l'header della tabella, se presente
        if headers:
            self.set_font('Arial', 'B', 10) if bold_headers else self.set_font('Arial', '', 10)
            for header, width in zip(headers, col_widths):
                self.cell(width, 8, header, 1, 0, 'C')
            self.ln()

        self.set_font('Arial', '', 10)

        # Stampa ogni riga della tabella
        for row in data:
            # Calcola le altezze delle celle per ogni riga
            row_heights = [self.calculate_cell_height(datum, width) for datum, width in zip(row, col_widths)]
            max_row_height = max(row_heights)  # Trova l'altezza massima della riga

            print(max_row_height, "max row of table")

            # Verifica se la prossima riga si adatta alla pagina
            if self.get_y() + max_row_height > self.page_break_trigger:
                self.add_page()
                start_y = self.get_y()  # Aggiorna la posizione di inizio sulla nuova pagina

            # Inizia a stampare le celle nella loro posizione originale
            x_start = self.get_x()
            y_start = self.get_y()
            for i, (datum, width) in enumerate(zip(row, col_widths)):
                cell_height = row_heights[i]

                if cell_height == max_row_height:
                    print(cell_height, datum, "max row of table script")
                    self.multi_cell(width, 6, str(datum) if str(datum).strip() != "" else "-", 1, 'L', False)

                # Usa sempre multi_cell per tutte le celle

                # Aggiungi righe vuote sotto, solo se l'altezza della cella è minore della massima
                if cell_height < max_row_height:
                    print(cell_height, datum, "row of table script")
                    self.multi_cell(width, 6, str(datum) if str(datum).strip() != "" else "-", 'LTR', 'L', False)
                    empty_space = max_row_height - cell_height
                    self.set_xy(x_start, self.get_y())  # Mantieni la stessa posizione in x
                    self.multi_cell(width, empty_space, "", 'LBR', 'L', False)

                # Aggiorna la posizione x dopo ogni cella
                x_start += width
                self.set_xy(x_start, y_start)

            # Sposta la posizione in basso di max_row_height
            self.ln(max_row_height)

        # Salva la posizione di Y alla fine della tabella
        end_y = self.get_y()
        print(end_y, "end table")
        return end_y

    # Utilizzare la funzione draw_table nei metodi

    def calculate_cell_height(self, text, width):
        """ Calcola l'altezza necessaria per la cella in base alla larghezza e al testo. """
        self.set_font('Arial', '', 10)  # Imposta il font per il calcolo corretto
        if not text.strip():
            return 6  # Restituisce l'altezza minima se il testo è vuoto

        # Spezza il testo in parole
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            # Verifica se la riga corrente con la nuova parola supera la larghezza
            if self.get_string_width(current_line + word) <= width:
                current_line += word + " "
            else:
                # Aggiungi la riga corrente all'elenco delle righe e inizia una nuova riga
                lines.append(current_line)
                current_line = word + " "

        # Aggiungi eventuali righe dovute a "\n" nel testo
        lines.extend(text.split('\n'))

        # Calcola l'altezza totale: 6 punti per riga (o la tua altezza di riga preferita)
        return 6 * len(lines)

    def calculate_table_height(self, data, col_widths, headers=None):
        """ Calcola l'altezza totale della tabella per verificare se c'è spazio sufficiente sulla pagina. """
        total_height = 0

        # Aggiungi altezza dell'header se esiste
        if headers:
            total_height += 8  # Altezza standard dell'header

        # Calcola l'altezza totale delle righe
        for row in data:
            row_heights = [self.calculate_cell_height(datum, width) for datum, width in zip(row, col_widths)]
            total_height += max(row_heights)

        return total_height

    def invoice_header(self, invoice):
        self.set_font('Arial', '', 10)
        data = [
            [f"Document: DDT", f"n. {invoice['number']}", f"Data: {invoice['Date_1']}"]
        ]
        col_widths = [70, 40, 70]  # Regola le larghezze delle colonne come necessario
        self.set_y(self.get_y())  # Assicurati che inizi dopo la sezione precedente
        end_y = self.draw_table(data, col_widths, bold_headers=True)  # Salva la posizione finale Y
        self.set_y(end_y)

    def customer_details(self, invoice):
        data = [
            ["Goods destination:\n" + invoice["customer_phone"], "Customer:\n" + invoice["customer_address"]],
        ]
        col_widths = [70, 110]  # Regola le larghezze delle colonne come necessario
        self.set_y(self.get_y())  # Assicurati che inizi dopo la sezione precedente
        end_y = self.draw_table(data, col_widths, bold_headers=True)  # Salva la posizione finale Y
        self.set_y(end_y)

    def customer_details_1(self, invoice):
        data = [
            ["ID:\n" + " ", "Email:\n" + " ", "VAT:\n" + invoice["vat_number"]],
        ]
        col_widths = [25, 65, 90]  # Regola le larghezze delle colonne come necessario
        self.set_y(self.get_y())  # Assicurati che inizi dopo la sezione precedente
        end_y = self.draw_table(data, col_widths, bold_headers=True)  # Salva la posizione finale Y
        self.set_y(end_y)

    def agent_details(self, invoice):
        data = [
            ["Agent:\n" + " ", "Payment Condition:\n" + invoice["payment_condition"],
             "Shipment:\n" + invoice["sender_name"]]
        ]
        col_widths = [55, 35, 90]
        self.set_font('Arial', '', 8)
        self.set_y(self.get_y())  # Assicurati che inizi dopo la sezione precedente
        end_y = self.draw_table(data, col_widths, bold_headers=True)  # Salva la posizione finale Y
        self.set_y(end_y)

    def product_table(self, products):
        headers = ["Article", "Description", "Quantity", "Price", "1° Disc %", "2° %", "3° %", "Amount"]
        data = [
            [product['article'], product['product_description'], str(product['product_quantity']),
             str(product['product_price']), str(product['product_discount']), str(product['product_discount_2']),
             str(product['product_discount_3']), str(product['product_amount'])]
            for product in products
        ]
        col_widths = [20, 60, 20, 20, 20, 10, 10, 20]
        self.set_font('Arial', 'B', 10)
        self.cell(0, 8, 'Product Details', 0, 1, 'L')
        self.set_y(self.get_y())  # Assicurati che inizi dopo la sezione precedente
        end_y = self.draw_table(data, col_widths, bold_headers=True)  # Salva la posizione finale Y
        self.set_y(end_y)

    def total_details(self, invoice):
        data = [
            ["Total Quantity:\n" + str(invoice["total_quantity"]), "IVA:\n" + " ",
             "Sender:\n" + invoice["sender_name"]],
            ["Reason for export:\n" + "Vendita", "Courier Service:\n" + " ", "Recipient:\n" + invoice["recipient"]],
            ["Total Amount:\n" + str(invoice["total_amount"]), "IVA Amount:\n" + "Art.8 com.1 DPR n.633/72 ",
             "Total Invoice EURO:\n" + str(invoice["total_invoice_euro"])],
        ]
        col_widths = [60, 60, 60]
        self.set_font('Arial', 'B', 10)
        self.cell(0, 8, 'Total Details', 0, 1, 'L')
        self.set_y(self.get_y())  # Assicurati che inizi dopo la sezione precedente
        end_y = self.draw_table(data, col_widths, bold_headers=True)  # Salva la posizione finale Y
        self.set_y(end_y)

    def thank_you_details(self, invoice):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 8, 'Thank you for choosing our products!', 0, 1, 'R')

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
def generate_non_sold_pdf(order):
    invoice_number = order[0]
    invoice = fetch_invoice_data(invoice_number)
    products = fetch_invoice_products(invoice_number)
    if not invoice:
        messagebox.showerror("Errore", "Dati del documento non trovati.")
        return

    # Modifica i dettagli specifici per la bolla di non venduto
    def edit_and_confirm():
        def save_changes():
            # Associa il messagebox al popup come finestra genitore
            messagebox.showinfo("Attenzione", "Dati della fattura salvati.", parent=popup)
            #funzione che salva le info su DB
        def save_changes_and_print():
            # Update invoice data from the entry fields
            invoice["number"] = entry_number.get()
            invoice["Date_1"] = entry_date.get()
            invoice["customer_phone"] = entry_customer_phone.get()
            invoice["customer_address"] = entry_customer_address.get()
            invoice["vat_number"] = entry_vat_number.get()
            invoice["payment_condition"] = entry_payment_condition.get()
            invoice["sender_name"] = entry_sender_name.get()
            invoice["courier_service"] = entry_courier_service.get()
            invoice["recipient"] = entry_recipient.get()
            invoice["total_quantity"] = entry_total_quantity.get()
            # invoice["iva_amount"] = entry_iva_amount.get()
            invoice["total_amount"] = entry_total_amount.get()
            invoice["total_invoice_euro"] = entry_total_invoice_euro.get()

            for i, product in enumerate(products):
                product["article"] = format_field(product_entries[i]["article"].get())
                product["product_description"] = format_field(product_entries[i]["description"].get())
                product["product_quantity"] = format_field(product_entries[i]["quantity"].get())
                product["product_price"] = format_field(product_entries[i]["price"].get())
                product["product_discount"] = format_field(product_entries[i]["discount"].get())
                product["product_amount"] = format_field(product_entries[i]["amount"].get())

            # Close the popup window after saving changes
            popup.destroy()

            # Open a separate window to choose save path
            choose_save_path()

        # Ottiene la data corrente e la formatta come YYYYMMDD
        current_date = datetime.now().strftime("%Y%m%d")
        filename = f"Bolla_DDT_{current_date}"

        def choose_save_path():
            save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")],
                                                     initialfile=filename)
            if save_path:
                pdf = PDFNonSold()
                pdf.add_page()
                pdf.invoice_header(invoice)
                pdf.customer_details(invoice)
                pdf.customer_details_1(invoice)
                pdf.agent_details(invoice)
                pdf.product_table(products)
                pdf.total_details(invoice)
                pdf.thank_you_details(invoice)
                pdf.add_footer_on_last_page()
                pdf.output(save_path)
                messagebox.showinfo("Successo", f"Bolla di non venduto salvata come {os.path.basename(save_path)}")
            else:
                messagebox.showwarning("Salvataggio Annullato",
                                       "Il salvataggio della bolla di non venduto è stato annullato.")

        # Create the popup window
        popup = tk.Toplevel()
        popup.title("Modifica i dettagli della bolla di non venduto")
        popup.geometry("1700x650")  # Set the size of the popup window
        popup.resizable(True, True)  # Prevent resizing for consistent layout

        data_frame = tk.Frame(popup)
        data_frame.grid(row=0, column=0, columnspan=2)

        # padding = {'padx': 5, 'pady': 1}
        product_frame = tk.Frame(popup)
        product_frame.grid(row=0, column=2, columnspan=5)

        # Add padding and spacing between elements
        padding = {'padx': 10, 'pady': 5}
        # Set the width of entry fields and the font size
        entry_width = 40
        font_size = ("Arial", 14)  # Font family Arial, size 14

        # Create and grid labels and entries for each invoice field with larger font
        tk.Label(data_frame, text="Numero:", font=font_size).grid(row=0, column=0, **padding)
        entry_number = tk.Entry(data_frame, width=entry_width, font=font_size)
        entry_number.grid(row=0, column=1, **padding)
        entry_number.insert(0, invoice["number"])

        tk.Label(data_frame, text="Data:", font=font_size).grid(row=1, column=0, **padding)
        entry_date = tk.Entry(data_frame, width=entry_width, font=font_size)
        entry_date.grid(row=1, column=1, **padding)
        entry_date.insert(0, invoice["Date_1"])

        tk.Label(data_frame, text="Telefono Cliente:", font=font_size).grid(row=2, column=0, **padding)
        entry_customer_phone = tk.Entry(data_frame, width=entry_width, font=font_size)
        entry_customer_phone.grid(row=2, column=1, **padding)
        entry_customer_phone.insert(0, invoice["customer_phone"])

        tk.Label(data_frame, text="Indirizzo Cliente:", font=font_size).grid(row=3, column=0, **padding)
        entry_customer_address = tk.Entry(data_frame, width=entry_width, font=font_size)
        entry_customer_address.grid(row=3, column=1, **padding)
        entry_customer_address.insert(0, invoice["customer_address"])

        tk.Label(data_frame, text="Partita IVA:", font=font_size).grid(row=6, column=0, **padding)
        entry_vat_number = tk.Entry(data_frame, width=entry_width, font=font_size)
        entry_vat_number.grid(row=6, column=1, **padding)
        entry_vat_number.insert(0, invoice["vat_number"])

        tk.Label(data_frame, text="Condizioni di Pagamento:", font=font_size).grid(row=11, column=0, **padding)
        entry_payment_condition = tk.Entry(data_frame, width=entry_width, font=font_size)
        entry_payment_condition.grid(row=11, column=1, **padding)
        entry_payment_condition.insert(0, invoice["payment_condition"])

        tk.Label(data_frame, text="Mittente:", font=font_size).grid(row=12, column=0, **padding)
        entry_sender_name = tk.Entry(data_frame, width=entry_width, font=font_size)
        entry_sender_name.grid(row=12, column=1, **padding)
        entry_sender_name.insert(0, invoice["sender_name"])

        tk.Label(data_frame, text="Servizio di Corriere:", font=font_size).grid(row=14, column=0, **padding)
        entry_courier_service = tk.Entry(data_frame, width=entry_width, font=font_size)
        entry_courier_service.grid(row=14, column=1, **padding)
        entry_courier_service.insert(0, invoice["courier_service"])

        tk.Label(data_frame, text="Destinatario:", font=font_size).grid(row=15, column=0, **padding)
        entry_recipient = tk.Entry(data_frame, width=entry_width, font=font_size)
        entry_recipient.grid(row=15, column=1, **padding)
        entry_recipient.insert(0, invoice["recipient"])

        tk.Label(data_frame, text="Quantità Totale:", font=font_size).grid(row=16, column=0, **padding)
        entry_total_quantity = tk.Entry(data_frame, width=entry_width, font=font_size)
        entry_total_quantity.grid(row=16, column=1, **padding)
        entry_total_quantity.insert(0, invoice["total_quantity"])

        tk.Label(data_frame, text="IVA:", font=font_size).grid(row=17, column=0, **padding)
        entry_iva_amount = tk.Entry(data_frame, width=entry_width, font=font_size)
        entry_iva_amount.grid(row=17, column=1, **padding)
        entry_iva_amount.insert(0, invoice["iva_amount"])

        tk.Label(data_frame, text="Importo Totale:", font=font_size).grid(row=18, column=0, **padding)
        entry_total_amount = tk.Entry(data_frame, width=entry_width, font=font_size)
        entry_total_amount.grid(row=18, column=1, **padding)
        entry_total_amount.insert(0, invoice["total_amount"])

        tk.Label(data_frame, text="Totale Fattura EURO:", font=font_size).grid(row=19, column=0, **padding)
        entry_total_invoice_euro = tk.Entry(data_frame, width=entry_width, font=font_size)
        entry_total_invoice_euro.grid(row=19, column=1, **padding)
        entry_total_invoice_euro.insert(0, invoice["total_invoice_euro"])

        def calculate_total_amount():
            total = 0.0
            for product_entry in product_entries:
                try:
                    quantity = float(product_entry["quantity"].get() or 0)
                    price = float(product_entry["price"].get() or 0)
                    discount1 = float(product_entry["discount"].get() or 0) / 100
                    # Calculate initial amount
                    amount = quantity * price

                    # Apply discounts sequentially
                    amount -= amount * discount1

                    # Update product's amount field
                    product_entry["amount"].config(state='normal')
                    product_entry["amount"].delete(0, tk.END)
                    product_entry["amount"].insert(0, f"{amount:.2f}")
                    product_entry["amount"].config(state='readonly')

                    # Add to total
                    total += amount
                except ValueError:
                    # Handle any entries that aren't valid numbers
                    pass
            entry_total_invoice_euro.config(state='normal')  # Enable editing to update value
            entry_total_invoice_euro.delete(0, tk.END)
            entry_total_invoice_euro.insert(0, f"{total:.2f}")
            entry_total_invoice_euro.config(state='readonly')  # Set back to readonly

        # Create entries for each product in a row
        product_entries = []
        for i, product in enumerate(products):
            row = 1 + i
            print(i)
            # Create headers for product fields
            tk.Label(product_frame, text="Articolo", font=font_size).grid(row=0, column=2, **padding)
            tk.Label(product_frame, text="Descrizione", font=font_size).grid(row=0, column=3, **padding)
            tk.Label(product_frame, text="Quantità", font=font_size).grid(row=0, column=4, **padding)
            tk.Label(product_frame, text="Prezzo", font=font_size).grid(row=0, column=5, **padding)
            tk.Label(product_frame, text="Sconto", font=font_size).grid(row=0, column=6, **padding)
            tk.Label(product_frame, text="Importo", font=font_size).grid(row=0, column=7, **padding)

            entry_article = tk.Entry(product_frame, width=10, font=font_size)
            entry_article.grid(row=1 + i, column=2, **padding)
            entry_article.insert(0, product["article"])

            entry_description = tk.Entry(product_frame, width=20, font=font_size)
            entry_description.grid(row=1 + i, column=3, **padding)
            entry_description.insert(0, product["product_description"])

            entry_quantity = tk.Entry(product_frame, width=10, font=font_size)
            entry_quantity.grid(row=1 + i, column=4, **padding)
            entry_quantity.insert(0, product["product_quantity"])
            entry_quantity.bind("<KeyRelease>", lambda e: calculate_total_amount())

            entry_price = tk.Entry(product_frame, width=10, font=font_size)
            entry_price.grid(row=1 + i, column=5, **padding)
            entry_price.insert(0, product["product_price"])
            entry_price.bind("<KeyRelease>", lambda e: calculate_total_amount())

            entry_discount = tk.Entry(product_frame, width=5, font=font_size)
            entry_discount.grid(row=1 + i, column=6, **padding)
            entry_discount.insert(0, product["product_discount"])
            entry_discount.bind("<KeyRelease>", lambda e: calculate_total_amount())

            entry_amount = tk.Entry(product_frame, width=10, font=font_size)
            entry_amount.grid(row=1 + i, column=7, **padding)
            entry_amount.insert(0, product["product_amount"])

            product_entries.append({
                "article": entry_article,
                "description": entry_description,
                "quantity": entry_quantity,
                "price": entry_price,
                "discount": entry_discount,
                "amount": entry_amount
            })

        def add_product():
            clienti = get_all_clienti_names()  # Da modificare
            condizione_selezionata = tk.StringVar()
            entry_article = ttk.Combobox(product_frame, textvariable=condizione_selezionata, values=clienti,
                                         font=font_size)
            entry_article.configure(width=15)
            entry_article.option_add('*TCombobox*Listbox*Font', font_size)
            entry_article.grid(row=len(product_entries) + 1, column=2, **padding)
            entry_article.bind("<<ComboboxSelected>>",
                               lambda event: update_description(entry_article, entry_description, entry_price))
            setup_incremental_search(entry_article, clienti)

            entry_description = tk.Entry(product_frame, width=20, font=font_size)
            entry_description.grid(row=len(product_entries) + 1, column=3, **padding)

            entry_quantity = tk.Entry(product_frame, width=10, font=font_size)
            entry_quantity.grid(row=len(product_entries) + 1, column=4, **padding)
            entry_quantity.bind("<KeyRelease>", lambda e: calculate_total_amount())

            entry_price = tk.Entry(product_frame, width=10, font=font_size)
            entry_price.grid(row=len(product_entries) + 1, column=5, **padding)
            entry_price.bind("<KeyRelease>", lambda e: calculate_total_amount())

            entry_discount = tk.Entry(product_frame, width=5, font=font_size)
            entry_discount.grid(row=len(product_entries) + 1, column=6, **padding)
            entry_discount.bind("<KeyRelease>", lambda e: calculate_total_amount())

            entry_amount = tk.Entry(product_frame, width=10, font=font_size)
            entry_amount.grid(row=len(product_entries) + 1, column=7, **padding)

            new_product = {
                "article": entry_article,
                "description": entry_description,
                "quantity": entry_quantity,
                "price": entry_price,
                "discount": entry_discount,
                "amount": entry_amount
            }
            new_entry = {
                "article": tk.StringVar(),
                "product_description": tk.StringVar(),
                "product_quantity": tk.StringVar(),
                "product_price": tk.StringVar(),
                "product_discount": tk.StringVar(),
                "product_amount": tk.StringVar()
            }
            products.append(new_entry)
            product_entries.append(new_product)  # Append this new entry reference to the product_entries list

        def remove_product():
            # Remove the last product from the list if there are any products
            if product_entries:
                last_entry_index = len(product_entries) - 1
                last_entry = product_entries.pop()  # Rimuove l'ultima riga aggiunta
                # Rimuove gli entry widget dalla grid
                last_entry["article"].grid_forget()
                last_entry["description"].grid_forget()
                last_entry["quantity"].grid_forget()
                last_entry["price"].grid_forget()
                last_entry["discount"].grid_forget()
                last_entry["amount"].grid_forget()
            if len(products) > last_entry_index:
                products.pop(last_entry_index)
            calculate_total_amount()

        def update_description(entry_article, entry_description, entry_price):
            article = entry_article.get()
            description = fetch_description_for_article(article)  # Query the description based on the article
            entry_description.delete(0, tk.END)
            entry_description.insert(0, description)
            price = fetch_price_for_article(article)
            entry_price.delete(0, tk.END)
            entry_price.insert(0, price)

        def fetch_price_for_article(article):
            conn = _connection()
            cursor = conn.cursor()
            cursor.execute("SELECT `CAP` FROM clienti WHERE `Ragione Sociale` = %s;", (article,))

            # Check if result is not None and access the first element of the tuple
            result = cursor.fetchone()  # Use fetchone() to get a single result directly
            conn.close()
            price = result[0] if result else ""
            return price

        def fetch_description_for_article(article):
            """ Get the names of all clienti from the 'clienti' table """
            conn = _connection()
            cursor = conn.cursor()
            cursor.execute("SELECT `Indirizzo` FROM clienti WHERE `Ragione Sociale` = %s;", (article,))
            # Check if result is not None and access the first element of the tuple
            result = cursor.fetchone()  # Use fetchone() to get a single result directly
            conn.close()
            description = result[0] if result else ""
            return description

        button_add = ctk.CTkButton(popup, text="Aggiungi Prodotto", command=add_product, font=font_size, width=120, height=30).grid(row=23, column=0,
                                                                                           **padding)
        button_remove = ctk.CTkButton(popup, text="Rimuovi Prodotto", command=remove_product, font=font_size, width=120, height=30).grid(row=23, column=1,
                                                                                               **padding)
        button_save = ctk.CTkButton(popup, text="Salva modifiche", command=save_changes, font=font_size, width=120,
                                    height=30).grid(row=23, column=2, **padding)
        button_save_and_print = ctk.CTkButton(popup, text="Salva modifiche e conferma", command=save_changes_and_print,
                                              font=font_size, width=120, height=30).grid(row=23, column=3, **padding)
        calculate_total_amount()

    edit_and_confirm()

    # Generazione del PDF della bolla di non venduto
    pdf = PDFNonSold()
    pdf.add_page()

    # Qui potresti voler modificare le intestazioni o altri dettagli
    pdf.invoice_header(invoice)  # Modifica il nome della funzione o il contenuto se necessario
    pdf.customer_details(invoice)
    pdf.customer_details_1(invoice)
    pdf.agent_details(invoice)
    pdf.product_table(products)
    pdf.total_details(invoice)
    pdf.thank_you_details(
        invoice)  # Anche qui potrebbero esserci modifiche per riflettere che è una bolla di non venduto

    # Salva il PDF nel percorso scelto
    choose_save_path = lambda: None  # Implementa una logica simile a quella esistente per salvare il PDF
    choose_save_path()