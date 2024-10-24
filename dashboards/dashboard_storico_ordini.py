import customtkinter as ctk
from tkinter import ttk, messagebox ,filedialog, Menu
import tkinter as tk
import sqlite3
import os
import datetime
from datetime import datetime
from fpdf import FPDF
from PIL import Image, ImageTk
import fitz
import xml.etree.ElementTree as ET
from dashboards.create_pdf_fattura import generate_invoice_pdf
from dashboards.create_pdf_non_sold import generate_non_sold_pdf
from dashboards.create_pdf_return import generate_return_pdf


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

def show_dashboard8(parent_frame):

    filter_frame = ctk.CTkFrame(parent_frame, corner_radius=5)
    filter_frame.pack(pady=5, padx=5, fill="x")
    global combobox

    #selected_cliente = tk.StringVar()

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
        conn = sqlite3.connect('Database_Utilities/Database/MergedDatabase.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT DISTINCT {column_name} FROM storico_ordini")
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
        conn = sqlite3.connect('Database_Utilities/Database/MergedDatabase.db')
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

    def print_invoice():
        selected_item = tree.selection()
        if selected_item:
            order = tree.item(selected_item, "values")
            generate_invoice_pdf(order)
        else:
            messagebox.showwarning("Seleziona Ordine", "Per favore, seleziona un ordine per stampare la fattura.")

    def fetch_invoice_data(invoice_number):
        conn = sqlite3.connect('resources/orders_fattura_1.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM orders_fattura_newfields WHERE id = '{invoice_number}'")
        column_names = [description[0] for description in cursor.description]
        invoice_tuple = cursor.fetchone()
        conn.close()
        if invoice_tuple:
            invoice = dict(zip(column_names, invoice_tuple))
            return invoice
        return None

    def fetch_invoice_products(invoice_number):
        conn = sqlite3.connect('resources/orders_fattura_1.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT article, product_description, product_quantity,product_price, product_discount,product_discount_2,product_discount_3, product_amount FROM orders_fattura_newfields WHERE id = '{invoice_number}'")
        column_names = [description[0] for description in cursor.description]
        product_rows = cursor.fetchall()
        conn.close()
        products = [dict(zip(column_names, product_row)) for product_row in product_rows]
        return products


    def print_non_sold_document():
        selected_item = tree.selection()
        if selected_item:
            order = tree.item(selected_item, "values")
            generate_non_sold_pdf(order)
        else:
            messagebox.showwarning("Seleziona Ordine",
                                   "Per favore, seleziona un ordine per stampare la bolla di non venduto.")


    parent_frame.grid_columnconfigure(0, weight=1)
    parent_frame.grid_columnconfigure(1, weight=1)

    button = ctk.CTkButton(parent_frame, text="Stampa Fattura", command=print_invoice)
    button.pack(side="left", padx=10, pady=20)

    button_non_sold = ctk.CTkButton(parent_frame, text="Stampa Bolla di non venduto", command=print_non_sold_document)
    button_non_sold.pack(side="left", padx=10, pady=20)

    def print_return_document():
        selected_item = tree.selection()
        if selected_item:
            order = tree.item(selected_item, "values")
            generate_return_pdf(order)
        else:
            messagebox.showwarning("Seleziona Ordine",
                                   "Per favore, seleziona un ordine per stampare la bolla di reso.")

    button_return = ctk.CTkButton(parent_frame, text="Stampa Bolla di reso", command=print_return_document)
    button_return.pack(side="left", padx=10, pady=20)

    def create_invoice_xml(id_trasmittente, codice_trasmittente, progressivo_invio, codice_destinatario,
                           cedente_id_codice, cedente_codice_fiscale, cedente_nome, cedente_cognome,
                           cedente_regime_fiscale, cedente_indirizzo, cedente_numero_civico, cedente_cap,
                           cedente_comune, cedente_provincia, cedente_nazione, cedente_email,
                           cessionario_id_codice, cessionario_codice_fiscale, cessionario_denominazione,
                           cessionario_indirizzo, cessionario_cap, cessionario_comune, cessionario_provincia,
                           cessionario_nazione, tipo_documento, data_documento, numero_documento,
                           importo_totale_documento, descrizione, quantita, prezzo_unitario, aliquota_iva,
                           importo_pagamento, data_scadenza_pagamento, modalita_pagamento):

        try:
            quantita = float(quantita)  # o int(quantita) se è sempre un numero intero
            prezzo_unitario = float(prezzo_unitario)
            importo_totale_documento = float(importo_totale_documento)
            importo_pagamento = float(importo_pagamento)
            aliquota_iva = float(aliquota_iva)
        except ValueError:
            raise ValueError("Uno o più valori numerici sono invalidi.")
        fattura = ET.Element('FatturaElettronica',
                             xmlns="http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2", versione="FPR12")

        # Header
        header = ET.SubElement(fattura, 'FatturaElettronicaHeader')
        dati_trasmissione = ET.SubElement(header, 'DatiTrasmissione')
        id_trasmittente = ET.SubElement(dati_trasmissione, 'IdTrasmittente')
        ET.SubElement(id_trasmittente, 'IdPaese').text = 'IT'
        ET.SubElement(id_trasmittente, 'IdCodice').text = id_trasmittente
        ET.SubElement(dati_trasmissione, 'ProgressivoInvio').text = progressivo_invio
        ET.SubElement(dati_trasmissione, 'FormatoTrasmissione').text = 'FPR12'
        ET.SubElement(dati_trasmissione, 'CodiceDestinatario').text = codice_destinatario

        cedente_prestatore = ET.SubElement(header, 'CedentePrestatore')
        dati_anagrafici = ET.SubElement(cedente_prestatore, 'DatiAnagrafici')
        id_fiscale_iva = ET.SubElement(dati_anagrafici, 'IdFiscaleIVA')
        ET.SubElement(id_fiscale_iva, 'IdPaese').text = 'IT'
        ET.SubElement(id_fiscale_iva, 'IdCodice').text = cedente_id_codice
        ET.SubElement(dati_anagrafici, 'CodiceFiscale').text = cedente_codice_fiscale
        anagrafica = ET.SubElement(dati_anagrafici, 'Anagrafica')
        ET.SubElement(anagrafica, 'Nome').text = cedente_nome
        ET.SubElement(anagrafica, 'Cognome').text = cedente_cognome
        ET.SubElement(dati_anagrafici, 'RegimeFiscale').text = cedente_regime_fiscale

        sede = ET.SubElement(cedente_prestatore, 'Sede')
        ET.SubElement(sede, 'Indirizzo').text = cedente_indirizzo
        ET.SubElement(sede, 'NumeroCivico').text = cedente_numero_civico
        ET.SubElement(sede, 'CAP').text = cedente_cap
        ET.SubElement(sede, 'Comune').text = cedente_comune
        ET.SubElement(sede, 'Provincia').text = cedente_provincia
        ET.SubElement(sede, 'Nazione').text = cedente_nazione

        contatti = ET.SubElement(cedente_prestatore, 'Contatti')
        ET.SubElement(contatti, 'Email').text = cedente_email

        cessionario_committente = ET.SubElement(header, 'CessionarioCommittente')
        dati_anagrafici = ET.SubElement(cessionario_committente, 'DatiAnagrafici')
        id_fiscale_iva = ET.SubElement(dati_anagrafici, 'IdFiscaleIVA')
        ET.SubElement(id_fiscale_iva, 'IdPaese').text = 'IT'
        ET.SubElement(id_fiscale_iva, 'IdCodice').text = cessionario_id_codice
        ET.SubElement(dati_anagrafici, 'CodiceFiscale').text = cessionario_codice_fiscale
        anagrafica = ET.SubElement(dati_anagrafici, 'Anagrafica')
        ET.SubElement(anagrafica, 'Denominazione').text = cessionario_denominazione

        sede = ET.SubElement(cessionario_committente, 'Sede')
        ET.SubElement(sede, 'Indirizzo').text = cessionario_indirizzo
        ET.SubElement(sede, 'CAP').text = cessionario_cap
        ET.SubElement(sede, 'Comune').text = cessionario_comune
        ET.SubElement(sede, 'Provincia').text = cessionario_provincia
        ET.SubElement(sede, 'Nazione').text = cessionario_nazione

        # Body
        body = ET.SubElement(fattura, 'FatturaElettronicaBody')
        dati_generali = ET.SubElement(body, 'DatiGenerali')
        dati_generali_documento = ET.SubElement(dati_generali, 'DatiGeneraliDocumento')
        ET.SubElement(dati_generali_documento, 'TipoDocumento').text = tipo_documento
        ET.SubElement(dati_generali_documento, 'Divisa').text = 'EUR'
        ET.SubElement(dati_generali_documento, 'Data').text = data_documento
        ET.SubElement(dati_generali_documento, 'Numero').text = numero_documento
        ET.SubElement(dati_generali_documento, 'ImportoTotaleDocumento').text = str(importo_totale_documento)

        dati_beni_servizi = ET.SubElement(body, 'DatiBeniServizi')
        dettaglio_linee = ET.SubElement(dati_beni_servizi, 'DettaglioLinee')
        ET.SubElement(dettaglio_linee, 'NumeroLinea').text = '1'
        ET.SubElement(dettaglio_linee, 'Descrizione').text = descrizione
        ET.SubElement(dettaglio_linee, 'Quantita').text = str(quantita)
        ET.SubElement(dettaglio_linee, 'PrezzoUnitario').text = str(prezzo_unitario)
        ET.SubElement(dettaglio_linee, 'PrezzoTotale').text = str(prezzo_unitario * quantita)
        ET.SubElement(dettaglio_linee, 'AliquotaIVA').text = str(aliquota_iva)

        dati_riepilogo = ET.SubElement(dati_beni_servizi, 'DatiRiepilogo')
        ET.SubElement(dati_riepilogo, 'AliquotaIVA').text = str(aliquota_iva)
        ET.SubElement(dati_riepilogo, 'ImponibileImporto').text = str(prezzo_unitario * quantita)
        ET.SubElement(dati_riepilogo, 'Imposta').text = str(prezzo_unitario * quantita * aliquota_iva / 100)

        dati_pagamento = ET.SubElement(body, 'DatiPagamento')
        condizioni_pagamento = ET.SubElement(dati_pagamento, 'CondizioniPagamento').text = 'TP02'
        dettaglio_pagamento = ET.SubElement(dati_pagamento, 'DettaglioPagamento')
        ET.SubElement(dettaglio_pagamento, 'ModalitaPagamento').text = modalita_pagamento
        ET.SubElement(dettaglio_pagamento, 'DataScadenzaPagamento').text = data_scadenza_pagamento
        ET.SubElement(dettaglio_pagamento, 'ImportoPagamento').text = str(importo_pagamento)

        # Convert to XML string
        tree = ET.ElementTree(fattura)
        ET.indent(tree, space="\t", level=0)
        xml_string = ET.tostring(fattura, encoding='unicode')
        return xml_string

    def show_invoice_form():
        def save_invoice():
            dati = {key: entry.get() for key, entry in entries.items()}
            invoice_xml = create_invoice_xml(**dati)
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xml",
                filetypes=[("XML files", "*.xml")],
                initialfile="Fattura.xml"
            )
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(invoice_xml)
                messagebox.showinfo("Successo", "Fattura salvata correttamente.")
            else:
                messagebox.showwarning("Annullato", "Salvataggio file annullato.")

        popup = tk.Toplevel()
        popup.title("Conferma Dati Fattura XML")
        popup.geometry("800x800")  # Imposta un'altezza sufficiente per vedere il pulsante

        # Crea un Canvas e uno Scrollbar
        canvas = tk.Canvas(popup)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(popup, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)

        # Crea un Frame all'interno del Canvas
        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor='nw')

        entries = {}

        fields = [
            "ID Trasmittente", "Codice Trasmittente", "Progressivo Invio", "Codice Destinatario",
            "Cedente ID Codice", "Cedente Codice Fiscale", "Cedente Nome", "Cedente Cognome",
            "Cedente Regime Fiscale", "Cedente Indirizzo", "Cedente Numero Civico", "Cedente CAP",
            "Cedente Comune", "Cedente Provincia", "Cedente Nazione", "Cedente Email",
            "Cessionario ID Codice", "Cessionario Codice Fiscale", "Cessionario Denominazione",
            "Cessionario Indirizzo", "Cessionario CAP", "Cessionario Comune", "Cessionario Provincia",
            "Cessionario Nazione", "Tipo Documento", "Data Documento", "Numero Documento",
            "Importo Totale Documento", "Descrizione", "Quantita", "Prezzo Unitario", "Aliquota IVA",
            "Importo Pagamento", "Data Scadenza Pagamento", "Modalita Pagamento"
        ]

        example_data = [
            "IT12345678901", "12345678901", "001", "ABCDE",
            "98765432109", "98765432109", "Mario", "Rossi",
            "RF01", "Via Roma 1", "10", "00100",
            "Roma", "RM", "IT", "info@aziendatest.it",
            "123456789012", "123456789012", "Azienda Destinatario S.p.A.",
            "Via Milano 2", "00200", "Milano", "MI",
            "IT", "TD01", "2024-09-25", "2024/0001",
            "1000.50", "Vendita prodotti", "10", "100.05", "22",
            "1000.50", "2024-10-25", "MP01"
        ]

        # Set the width of entry fields and the font size
        entry_width = 40
        font_size = ("Arial", 14)  # Font family Arial, size 14

        for idx, (field, data) in enumerate(zip(fields, example_data)):
            label = tk.Label(frame, text=field, width=entry_width, font=font_size)
            label.grid(row=idx, column=0, padx=10, pady=2, sticky=tk.W)
            entry = tk.Entry(frame, width=entry_width, font=font_size)
            entry.grid(row=idx, column=1, padx=10, pady=2, sticky=tk.EW)
            entry.insert(0, data)
            entries[field.replace(" ", "_").lower()] = entry

        save_button = tk.Button(frame, text="Salva Fattura", command=save_invoice, font=font_size)
        save_button.grid(row=len(fields), columnspan=2, pady=20)

        frame.update_idletasks()  # Aggiorna lo stato del frame per calcolare la regione dello scroll

        canvas.config(scrollregion=canvas.bbox("all"))  # Aggiorna la regione dello scroll nel canvas

    button_xml = ctk.CTkButton(parent_frame, text="Stampa Fattura XML", command=show_invoice_form)
    button_xml.pack(side="left", padx=10, pady=20)

    class PDFSigarette(FPDF):
        def header_top(self):
            self.set_font('Arial', 'B', 14)
            self.cell(200, 10, txt="Documento Fattura", ln=True, align='C')
            # Aggiungi la data corrente nel formato GG/MM/AAAA
            current_date = datetime.now().strftime("%d/%m/%Y")
            self.cell(200, 10, txt=f"Data: {current_date}", ln=True, align='C')

            # Spazio aggiuntivo dopo l'intestazione
            self.ln(10)

        def add_table_headers(self):
            self.set_font('Arial', 'B', 10)
            self.cell(20, 10, 'Codice', 1, align='C')
            self.cell(70, 10, 'Descrizione', 1, align='C')
            self.cell(20, 10, 'Quantità', 1, align='C')
            self.cell(20, 10, 'Prezzo', 1, align='C')
            self.cell(30, 10, 'Sconto/Magg.', 1, align='C')
            self.cell(20, 10, 'Importo', 1, align='C')
            self.ln()

        def add_table_row(self, codice, descrizione, quantita, prezzo, sconto, importo):
            self.set_font('Arial', '', 10)
            self.cell(20, 10, codice if codice else '', 1, align='C')
            self.cell(70, 10, descrizione if descrizione else '', 1, align='C')
            self.cell(20, 10, quantita if quantita else '', 1, align='C')
            self.cell(20, 10, prezzo if prezzo else '', 1, align='C')
            self.cell(30, 10, sconto if sconto else '', 1, align='C')
            self.cell(20, 10, importo if importo else '', 1, align='C')


        def add_extra_fields(self, esistenza, disponibilita, trasporto, imballo, varie, bollo, totale_merce,
                             totale_quantita, totale_fattura):
            self.set_font('Arial', 'B', 10)
            self.ln(20)
            self.cell(50, 10, f"Esistenza: {esistenza}", 0, 0, align='C')
            self.cell(50, 10, f"Disponibilità: {disponibilita}", 0, 0, align='C')
            self.cell(50, 10, f"Trasporto: {trasporto}", 0, 1, align='C')
            self.cell(50, 10, f"Imballo: {imballo}", 0, 0, align='C')
            self.cell(50, 10, f"Varie: {varie}", 0, 0, align='C')
            self.cell(50, 10, f"Bollo: {bollo}", 0, 1, align='C')
            self.cell(50, 10, f"Totale Merce: {totale_merce}", 0, 0, align='C')
            self.cell(50, 10, f"Totale Quantità: {totale_quantita}", 0, 0, align='C')
            self.cell(50, 10, f"Totale Fattura: {totale_fattura}", 0, 1, align='C')

    def generate_pdf_sigaretta():
        # Popup window to edit and confirm invoice data
        def edit_and_confirm():
            def save_changes():
                # Salva i valori dei campi extra
                esistenza = entry_esistenza.get()
                disponibilita = entry_disponibilita.get()
                trasporto = entry_trasporto.get()
                imballo = entry_imballo.get()
                varie = entry_varie.get()
                bollo = entry_bollo.get()
                totale_merce = entry_totale_merce.get()
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
                choose_save_path(esistenza, disponibilita, trasporto, imballo, varie, bollo, totale_merce,
                                 totale_quantita, totale_fattura, products)

            # Ottiene la data corrente e la formatta come YYYYMMDD
            current_date = datetime.now().strftime("%Y%m%d")
            filename = f"Fattura_Sigaretta_{current_date}"
            def choose_save_path(esistenza, disponibilita, trasporto, imballo, varie, bollo, totale_merce,
                                 totale_quantita, totale_fattura, products):
                save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], initialfile=filename)
                if save_path:
                    pdf = PDFSigarette()
                    pdf.add_page()
                    pdf.header_top()

                    # Aggiungi le intestazioni della tabella e i prodotti
                    pdf.add_table_headers()
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
            popup.geometry("1600x700")

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
                for col in range(6):  # 6 colonne (Codice, Descrizione, ecc.)
                    entry = tk.Entry(popup, width=entry_width, font=font_size)
                    entry.grid(row=row, column=col + 1, padx=0, pady=0)
                    row_entries.append(entry)
                entries.append(row_entries)

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

    button_sigaretta = ctk.CTkButton(parent_frame, text="Stampa Fattura Sigaretta", command=generate_pdf_sigaretta)
    button_sigaretta.pack(side="left", padx=10, pady=20)
