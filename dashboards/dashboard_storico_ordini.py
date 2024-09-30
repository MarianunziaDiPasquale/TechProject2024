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

    selected_cliente = tk.StringVar()

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
        conn = sqlite3.connect('resources/orders.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT DISTINCT {column_name} FROM orders")
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
    date = get_unique_values('data')
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
        conn = sqlite3.connect('resources/orders.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders")
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

    class PDF(FPDF):
        def header(self):

            # Aggiungi il logo in alto a sinistra
            self.image('C:/PROGETTO/myapp/resources/LogoCINCOTTI.jpg', 8, 2, 77, 44, 'JPG')  # Modifica il percorso e le dimensioni

            # Aggiungi l'immagine in alto a destra
            self.image('C:/PROGETTO/myapp/resources/Logojpeg.jpg', 120, 8, 77, 33, 'JPG')  # Modifica il percorso e le dimensioni

            self.ln(35)

        def footer(self):
            # Aggiungi l'immagine in basso al centro
            self.set_y(-40)  # Posiziona a 30 mm dal fondo della pagina
            self.image('C:/PROGETTO/myapp/resources/LOGOMOZZABELLAECINCOTTI.jpg', 75, self.get_y(), 70, 40,
                       'JPG')  # Modifica il percorso e le dimensioni

        def draw_table(self, data, col_widths, headers=None, bold_headers=False):
            if headers:
                if bold_headers:
                    self.set_font('Arial', 'B', 10)
                else:
                    self.set_font('Arial', '', 10)

                for header, width in zip(headers, col_widths):
                    self.cell(width, 8, header, 1, 0, 'C')
                self.ln()

            if bold_headers:
                self.set_font('Arial', '', 10)

            for row in data:
                # Prima passata per determinare l'altezza massima della riga
                row_heights = []
                for datum, width in zip(row, col_widths):
                    line_height = 6  # Altezza per linea, può essere aggiustata
                    num_lines = self.get_string_width(datum) / width  # Calcola il numero di righe necessarie
                    num_lines = datum.count('\n') + 1  # Contiamo le nuove linee
                    height = line_height * num_lines
                    row_heights.append(height)
                max_row_height = max(row_heights)  # Altezza massima tra tutte le celle della riga

                # Seconda passata per disegnare le celle con l'altezza della riga determinata
                x_start = self.get_x()  # Posizione iniziale X per la riga
                y_start = self.get_y()  # Posizione iniziale Y per la riga
                for datum, width in zip(row, col_widths):
                    # Disegna la cella utilizzando multi_cell per il testo con ritorni a capo
                    self.multi_cell(width, line_height, datum, 1, 'L', False)
                    # Posiziona il cursore all'inizio della prossima cella nella riga
                    self.set_xy(x_start + width, y_start)
                    x_start += width  # Avanza per la larghezza della cella
                self.ln(max_row_height)  # Salta alla prossima riga usando l'altezza massima

        def invoice_header(self, invoice):
            self.set_font('Arial', '', 10)
            data = [
                f"Document: INVOICE", f"n. {invoice['number']}", f"Data: {invoice['Date_1']}"
            ]
            col_widths = [70, 40, 70]  # Regola le larghezze delle colonne come necessario
            self.draw_table([data], col_widths)

        def customer_details(self, invoice):
            data = [
                ["Goods destination:\n" + invoice["customer_phone"], "Customer:\n" + invoice["customer_address"]],
            ]
            col_widths = [70, 110]  # Regola le larghezze delle colonne come necessario
            self.draw_table(data, col_widths, bold_headers=True)

        def customer_details_1(self, invoice):
            data = [
                ["ID:\n" + invoice["id"], "Email:\n" + invoice["customer_email"],"VAT:\n" + invoice["vat_number"],"Nation:\n" + invoice["nation"]],
            ]
            col_widths = [25,65,45,45]  # Regola le larghezze delle colonne come necessario
            self.draw_table(data, col_widths, bold_headers=True)

        def bank_details(self, invoice):
            data = [
                ["IBAN:\n"+invoice["iban"], "Swift:\n"+invoice["swift"]]
            ]
            col_widths = [90,90]
            self.set_font('Arial', '', 8)
            self.draw_table(data, col_widths, bold_headers=True)

        def agent_details(self, invoice):
            data = [
                ["Agent:\n"+ invoice["agent_name"],"Payment Condition:\n"+ invoice["payment_condition"],"Sender:\n"+ invoice["sender_name"], "Giorno di chiusura:\n"+ invoice["sender_giorno"]]
            ]
            col_widths = [55,35,45,45]
            self.set_font('Arial', '', 8)
            self.draw_table(data, col_widths, bold_headers=True)

        def product_table(self, products):
            headers = ["Article", "Description", "Quantity", "Price", "Discount", "Amount"]
            data = [
                [product['article'], product['product_description'], str(product['product_quantity']),
                 str(product['product_price']), str(product['product_discount']), str(product['product_amount'])]
                for product in products
            ]
            col_widths = [20, 70, 20, 20, 20, 30]
            self.set_font('Arial', 'B', 10)
            self.cell(0, 8, 'Product Details', 0, 1, 'L')
            self.draw_table(data, col_widths, headers, bold_headers=True)

        def total_details(self, invoice):
            data = [
                ["Total Quantity:\n" + str(invoice["total_quantity"]),"IVA:\n" + str(invoice["iva_amount"]), "Sender:\n" + invoice["sender_name"]],
                ["Reason for export:\n" + "Vendita","Courier Service:\n" + invoice["courier_service"],"Recipient:\n" + invoice["recipient"]],
                ["Total Amount:\n" + str(invoice["total_amount"]),"IVA Amount:\n" + str(invoice["iva_amount"]),"Total Invoice EURO:\n" + str(invoice["total_invoice_euro"])],
            ]
            col_widths = [60,60,60]
            self.set_font('Arial', 'B', 10)
            self.cell(0, 8, 'Total Details', 0, 1, 'L')
            self.draw_table(data, col_widths, bold_headers=True)

        def thank_you_details(self, invoice):
            self.set_font('Arial', 'B', 10)
            self.cell(0, 8, 'Thank you for choosing our products!', 0, 1, 'R')

    def fetch_invoice_data(invoice_number):
        conn = sqlite3.connect('resources/orders_fattura_1.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM orders_fattura WHERE id = '{invoice_number}'")
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
        cursor.execute(f"SELECT * FROM orders_fattura WHERE id = '{invoice_number}'")
        column_names = [description[0] for description in cursor.description]
        product_rows = cursor.fetchall()
        conn.close()
        products = [dict(zip(column_names, product_row)) for product_row in product_rows]
        return products

    def generate_invoice_pdf(order):
        invoice_number = order[0]
        invoice = fetch_invoice_data(invoice_number)
        products = fetch_invoice_products(invoice_number)
        if not invoice:
            messagebox.showerror("Errore", "Dati della fattura non trovati.")
            return

        # Popup window to edit and confirm invoice data
        def edit_and_confirm():
            def save_changes():
                # Update invoice data from the entry fields
                invoice["number"] = entry_number.get()
                invoice["Date_1"] = entry_date.get()
                invoice["customer_phone"] = entry_customer_phone.get()
                invoice["customer_address"] = entry_customer_address.get()
                invoice["id"] = entry_id.get()
                invoice["customer_email"] = entry_customer_email.get()
                invoice["vat_number"] = entry_vat_number.get()
                invoice["nation"] = entry_nation.get()
                invoice["iban"] = entry_iban.get()
                invoice["swift"] = entry_swift.get()
                invoice["agent_name"] = entry_agent_name.get()
                invoice["payment_condition"] = entry_payment_condition.get()
                invoice["sender_name"] = entry_sender_name.get()
                invoice["sender_giorno"] = entry_sender_giorno.get()
                invoice["courier_service"] = entry_courier_service.get()
                invoice["recipient"] = entry_recipient.get()
                invoice["total_quantity"] = entry_total_quantity.get()
                invoice["iva_amount"] = entry_iva_amount.get()
                invoice["total_amount"] = entry_total_amount.get()
                invoice["total_invoice_euro"] = entry_total_invoice_euro.get()

                for i, product in enumerate(products):
                    product["article"] = product_entries[i]["article"].get()
                    product["product_description"] = product_entries[i]["description"].get()
                    product["product_quantity"] = product_entries[i]["quantity"].get()
                    product["product_price"] = product_entries[i]["price"].get()
                    product["product_discount"] = product_entries[i]["discount"].get()
                    product["product_amount"] = product_entries[i]["amount"].get()

                # Close the popup window after saving changes
                popup.destroy()

                # Open a separate window to choose save path
                choose_save_path()

            # Ottiene la data corrente e la formatta come YYYYMMDD
            current_date = datetime.now().strftime("%Y%m%d")
            filename = f"Fattura_{current_date}"

            def choose_save_path():
                save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], initialfile=filename)
                if save_path:
                    pdf = PDF()
                    pdf.add_page()
                    pdf.invoice_header(invoice)
                    pdf.customer_details(invoice)
                    pdf.customer_details_1(invoice)
                    pdf.bank_details(invoice)
                    pdf.agent_details(invoice)
                    pdf.product_table(products)
                    pdf.total_details(invoice)
                    pdf.thank_you_details(invoice)
                    pdf.output(save_path)
                    show_pdf_preview(save_path)
                    messagebox.showinfo("Successo", f"Fattura salvata come {os.path.basename(save_path)}")
                else:
                    messagebox.showwarning("Salvataggio Annullato", "Il salvataggio della fattura è stato annullato.")

            # Create the popup window
            popup = tk.Toplevel()
            popup.title("Modifica i dettagli della fattura")
            popup.geometry("1700x850")  # Set the size of the popup window
            popup.resizable(True, True)  # Prevent resizing for consistent layout

            # Add padding and spacing between elements
            padding = {'padx': 10, 'pady': 5}
            # Set the width of entry fields and the font size
            entry_width = 40
            font_size = ("Arial", 14)  # Font family Arial, size 14

            # Create and grid labels and entries for each invoice field with larger font
            tk.Label(popup, text="Numero:", font=font_size).grid(row=0, column=0, **padding)
            entry_number = tk.Entry(popup, width=entry_width, font=font_size)
            entry_number.grid(row=0, column=1, **padding)
            entry_number.insert(0, invoice["number"])

            tk.Label(popup, text="Data:", font=font_size).grid(row=1, column=0, **padding)
            entry_date = tk.Entry(popup, width=entry_width, font=font_size)
            entry_date.grid(row=1, column=1, **padding)
            entry_date.insert(0, invoice["Date_1"])

            tk.Label(popup, text="Telefono Cliente:", font=font_size).grid(row=2, column=0, **padding)
            entry_customer_phone = tk.Entry(popup, width=entry_width, font=font_size)
            entry_customer_phone.grid(row=2, column=1, **padding)
            entry_customer_phone.insert(0, invoice["customer_phone"])

            tk.Label(popup, text="Indirizzo Cliente:", font=font_size).grid(row=3, column=0, **padding)
            entry_customer_address = tk.Entry(popup, width=entry_width, font=font_size)
            entry_customer_address.grid(row=3, column=1, **padding)
            entry_customer_address.insert(0, invoice["customer_address"])

            tk.Label(popup, text="ID:", font=font_size).grid(row=4, column=0, **padding)
            entry_id = tk.Entry(popup, width=entry_width, font=font_size)
            entry_id.grid(row=4, column=1, **padding)
            entry_id.insert(0, invoice["id"])

            tk.Label(popup, text="Email Cliente:", font=font_size).grid(row=5, column=0, **padding)
            entry_customer_email = tk.Entry(popup, width=entry_width, font=font_size)
            entry_customer_email.grid(row=5, column=1, **padding)
            entry_customer_email.insert(0, invoice["customer_email"])

            tk.Label(popup, text="Partita IVA:", font=font_size).grid(row=6, column=0, **padding)
            entry_vat_number = tk.Entry(popup, width=entry_width, font=font_size)
            entry_vat_number.grid(row=6, column=1, **padding)
            entry_vat_number.insert(0, invoice["vat_number"])

            tk.Label(popup, text="Nazione:", font=font_size).grid(row=7, column=0, **padding)
            entry_nation = tk.Entry(popup, width=entry_width, font=font_size)
            entry_nation.grid(row=7, column=1, **padding)
            entry_nation.insert(0, invoice["nation"])

            tk.Label(popup, text="IBAN:", font=font_size).grid(row=8, column=0, **padding)
            entry_iban = tk.Entry(popup, width=entry_width, font=font_size)
            entry_iban.grid(row=8, column=1, **padding)
            entry_iban.insert(0, invoice["iban"])

            tk.Label(popup, text="Swift:", font=font_size).grid(row=9, column=0, **padding)
            entry_swift = tk.Entry(popup, width=entry_width, font=font_size)
            entry_swift.grid(row=9, column=1, **padding)
            entry_swift.insert(0, invoice["swift"])

            tk.Label(popup, text="Agente:", font=font_size).grid(row=10, column=0, **padding)
            entry_agent_name = tk.Entry(popup, width=entry_width, font=font_size)
            entry_agent_name.grid(row=10, column=1, **padding)
            entry_agent_name.insert(0, invoice["agent_name"])

            tk.Label(popup, text="Condizioni di Pagamento:", font=font_size).grid(row=11, column=0, **padding)
            entry_payment_condition = tk.Entry(popup, width=entry_width, font=font_size)
            entry_payment_condition.grid(row=11, column=1, **padding)
            entry_payment_condition.insert(0, invoice["payment_condition"])

            tk.Label(popup, text="Mittente:", font=font_size).grid(row=12, column=0, **padding)
            entry_sender_name = tk.Entry(popup, width=entry_width, font=font_size)
            entry_sender_name.grid(row=12, column=1, **padding)
            entry_sender_name.insert(0, invoice["sender_name"])

            tk.Label(popup, text="Giorno di chiusura:", font=font_size).grid(row=13, column=0, **padding)
            entry_sender_giorno = tk.Entry(popup, width=entry_width, font=font_size)
            entry_sender_giorno.grid(row=13, column=1, **padding)
            entry_sender_giorno.insert(0, invoice["sender_giorno"])

            tk.Label(popup, text="Servizio di Corriere:", font=font_size).grid(row=14, column=0, **padding)
            entry_courier_service = tk.Entry(popup, width=entry_width, font=font_size)
            entry_courier_service.grid(row=14, column=1, **padding)
            entry_courier_service.insert(0, invoice["courier_service"])

            tk.Label(popup, text="Destinatario:", font=font_size).grid(row=15, column=0, **padding)
            entry_recipient = tk.Entry(popup, width=entry_width, font=font_size)
            entry_recipient.grid(row=15, column=1, **padding)
            entry_recipient.insert(0, invoice["recipient"])

            tk.Label(popup, text="Quantità Totale:", font=font_size).grid(row=16, column=0, **padding)
            entry_total_quantity = tk.Entry(popup, width=entry_width, font=font_size)
            entry_total_quantity.grid(row=16, column=1, **padding)
            entry_total_quantity.insert(0, invoice["total_quantity"])

            tk.Label(popup, text="IVA:", font=font_size).grid(row=17, column=0, **padding)
            entry_iva_amount = tk.Entry(popup, width=entry_width, font=font_size)
            entry_iva_amount.grid(row=17, column=1, **padding)
            entry_iva_amount.insert(0, invoice["iva_amount"])

            tk.Label(popup, text="Importo Totale:", font=font_size).grid(row=18, column=0, **padding)
            entry_total_amount = tk.Entry(popup, width=entry_width, font=font_size)
            entry_total_amount.grid(row=18, column=1, **padding)
            entry_total_amount.insert(0, invoice["total_amount"])

            tk.Label(popup, text="Totale Fattura EURO:", font=font_size).grid(row=19, column=0, **padding)
            entry_total_invoice_euro = tk.Entry(popup, width=entry_width, font=font_size)
            entry_total_invoice_euro.grid(row=19, column=1, **padding)
            entry_total_invoice_euro.insert(0, invoice["total_invoice_euro"])

            #padding = {'padx': 5, 'pady': 1}

            # Create headers for product fields
            tk.Label(popup, text="Articolo", font=font_size).grid(row=0, column=2, **padding)
            tk.Label(popup, text="Descrizione", font=font_size).grid(row=0, column=3, **padding)
            tk.Label(popup, text="Quantità", font=font_size).grid(row=0, column=4, **padding)
            tk.Label(popup, text="Prezzo", font=font_size).grid(row=0, column=5, **padding)
            tk.Label(popup, text="Sconto", font=font_size).grid(row=0, column=6,**padding)
            tk.Label(popup, text="Importo", font=font_size).grid(row= 0, column=7, **padding)

            # Create entries for each product in a row
            product_entries = []
            for i, product in enumerate(products):
                entry_article = tk.Entry(popup, width=10, font=font_size)
                entry_article.grid(row=1 + i, column=2, **padding)
                entry_article.insert(0, product["article"])

                entry_description = tk.Entry(popup, width=20, font=font_size)
                entry_description.grid(row=1 + i, column=3, **padding)
                entry_description.insert(0, product["product_description"])

                entry_quantity = tk.Entry(popup, width=10, font=font_size)
                entry_quantity.grid(row=1 + i, column=4, **padding)
                entry_quantity.insert(0, product["product_quantity"])

                entry_price = tk.Entry(popup, width=10, font=font_size)
                entry_price.grid(row=1 + i, column=5, **padding)
                entry_price.insert(0, product["product_price"])

                entry_discount = tk.Entry(popup, width=10, font=font_size)
                entry_discount.grid(row=1 + i, column=6, **padding)
                entry_discount.insert(0, product["product_discount"])

                entry_amount = tk.Entry(popup, width=10, font=font_size)
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

            # Add save changes button at the bottom
            tk.Button(popup, text="Salva modifiche e conferma", command=save_changes, font=font_size).grid(row=22, columnspan=2,
                                                                                           pady=30)

        edit_and_confirm()
        # Continue to generate the PDF after the popup is closed
        pdf = PDF()
        pdf.add_page()
        pdf.invoice_header(invoice)
        pdf.customer_details(invoice)
        pdf.customer_details_1(invoice)
        pdf.bank_details(invoice)
        pdf.agent_details(invoice)
        pdf.product_table(products)
        pdf.total_details(invoice)
        pdf.thank_you_details(invoice)



    def print_non_sold_document():
        selected_item = tree.selection()
        if selected_item:
            order = tree.item(selected_item, "values")
            generate_non_sold_pdf(order)
        else:
            messagebox.showwarning("Seleziona Ordine",
                                   "Per favore, seleziona un ordine per stampare la bolla di non venduto.")

    class PDFNonSold(FPDF):
        def header(self):

            # Aggiungi il logo in alto a sinistra
            self.image('C:/PROGETTO/myapp/resources/LogoCINCOTTI.jpg', 8, 2, 77, 44,
                       'JPG')  # Modifica il percorso e le dimensioni

            # Aggiungi l'immagine in alto a destra
            self.image('C:/PROGETTO/myapp/resources/Logojpeg.jpg', 120, 8, 77, 33,
                       'JPG')  # Modifica il percorso e le dimensioni

            self.ln(35)

        def footer(self):
            # Aggiungi l'immagine in basso al centro
            self.set_y(-40)  # Posiziona a 30 mm dal fondo della pagina
            self.image('C:/PROGETTO/myapp/resources/LOGOMOZZABELLAECINCOTTI.jpg', 75, self.get_y(), 70, 40,
                       'JPG')  # Modifica il percorso e le dimensioni

        def draw_table(self, data, col_widths, headers=None, bold_headers=False):
            if headers:
                self.set_font('Arial', 'B', 10) if bold_headers else self.set_font('Arial', '', 10)
                for header, width in zip(headers, col_widths):
                    self.cell(width, 8, header, 1, 0, 'C')
                self.ln()

            self.set_font('Arial', '', 10)

            for row in data:
                row_heights = [self.calculate_cell_height(datum, width) for datum, width in zip(row, col_widths)]
                max_row_height = max(row_heights)

                x_start = self.get_x()
                y_start = self.get_y()
                for datum, width in zip(row, col_widths):
                    self.multi_cell(width, 6, datum if datum.strip() != "" else "-", 1, 'L', False)
                    self.set_xy(x_start + width, y_start)
                    x_start += width
                self.ln(max_row_height)  # Move down to start the next row

        def calculate_cell_height(self, text, width):
            """ Calculate the necessary cell height for the text based on the column width. """
            self.set_font('Arial', '', 10)
            num_lines = max(1, self.get_string_width(text) / width)  # Ensure at least one line
            return 6 * (text.count('\n') + num_lines)  # Line height times the number of lines

        def invoice_header(self, invoice):
            self.set_font('Arial', '', 10)
            data = [
                f"Document: DDT", f"n. {invoice['number']}", f"Data: {invoice['Date_1']}"
            ]
            col_widths = [70, 40, 70]  # Regola le larghezze delle colonne come necessario
            self.draw_table([data], col_widths)

        def customer_details(self, invoice):
            data = [
                ["Goods destination:\n" + invoice["customer_phone"], "Customer:\n" + invoice["customer_address"]],
            ]
            col_widths = [70, 110]  # Regola le larghezze delle colonne come necessario
            self.draw_table(data, col_widths, bold_headers=True)

        def customer_details_1(self, invoice):
            data = [
                ["ID:\n" + " ", "Email:\n" + " ", "VAT:\n" + invoice["vat_number"]],
            ]
            col_widths = [25, 65, 90]  # Regola le larghezze delle colonne come necessario
            self.draw_table(data, col_widths, bold_headers=True)

        def agent_details(self, invoice):
            data = [
                ["Agent:\n" + " ", "Payment Condition:\n" + invoice["payment_condition"],
                 "Shipment:\n" + invoice["sender_name"]]
            ]
            col_widths = [55, 35, 90]
            self.set_font('Arial', '', 8)
            self.draw_table(data, col_widths, bold_headers=True)

        def product_table(self, products):
            headers = ["Article", "Description", "Quantity", "Price", "Discount", "Amount"]
            data = [
                [product['article'], product['product_description'], str(product['product_quantity']),
                 str(product['product_price']), str(product['product_discount']), str(product['product_amount'])]
                for product in products
            ]
            col_widths = [20, 70, 20, 20, 20, 30]
            self.set_font('Arial', 'B', 10)
            self.cell(0, 8, 'Product Details', 0, 1, 'L')
            self.draw_table(data, col_widths, headers, bold_headers=True)

        def total_details(self, invoice):
            data = [
                ["Total Quantity:\n" + str(invoice["total_quantity"]), "IVA:\n" + " ", "Sender:\n" + invoice["sender_name"]],
                ["Reason for export:\n" + "Vendita", "Courier Service:\n" + " ", "Recipient:\n" + invoice["recipient"]],
                ["Total Amount:\n" + str(invoice["total_amount"]), "IVA Amount:\n" + "Art.8 com.1 DPR n.633/72 ",
                 "Total Invoice EURO:\n" + str(invoice["total_invoice_euro"])],
            ]
            col_widths = [60, 60, 60]
            self.set_font('Arial', 'B', 10)
            self.cell(0, 8, 'Total Details', 0, 1, 'L')
            self.draw_table(data, col_widths, bold_headers=True)

        def thank_you_details(self, invoice):
            self.set_font('Arial', 'B', 10)
            self.cell(0, 8, 'Thank you for choosing our products!', 0, 1, 'R')

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
                #invoice["iva_amount"] = entry_iva_amount.get()
                invoice["total_amount"] = entry_total_amount.get()
                invoice["total_invoice_euro"] = entry_total_invoice_euro.get()

                for i, product in enumerate(products):
                    product["article"] = product_entries[i]["article"].get()
                    product["product_description"] = product_entries[i]["description"].get()
                    product["product_quantity"] = product_entries[i]["quantity"].get()
                    product["product_price"] = product_entries[i]["price"].get()
                    product["product_discount"] = product_entries[i]["discount"].get()
                    product["product_amount"] = product_entries[i]["amount"].get()

                # Close the popup window after saving changes
                popup.destroy()

                # Open a separate window to choose save path
                choose_save_path()

            # Ottiene la data corrente e la formatta come YYYYMMDD
            current_date = datetime.now().strftime("%Y%m%d")
            filename = f"Bolla_DDT_{current_date}"

            def choose_save_path():
                save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")],initialfile=filename)
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

            # Add padding and spacing between elements
            padding = {'padx': 10, 'pady': 5}
            # Set the width of entry fields and the font size
            entry_width = 40
            font_size = ("Arial", 14)  # Font family Arial, size 14

            # Create and grid labels and entries for each invoice field with larger font
            tk.Label(popup, text="Numero:", font=font_size).grid(row=0, column=0, **padding)
            entry_number = tk.Entry(popup, width=entry_width, font=font_size)
            entry_number.grid(row=0, column=1, **padding)
            entry_number.insert(0, invoice["number"])

            tk.Label(popup, text="Data:", font=font_size).grid(row=1, column=0, **padding)
            entry_date = tk.Entry(popup, width=entry_width, font=font_size)
            entry_date.grid(row=1, column=1, **padding)
            entry_date.insert(0, invoice["Date_1"])

            tk.Label(popup, text="Telefono Cliente:", font=font_size).grid(row=2, column=0, **padding)
            entry_customer_phone = tk.Entry(popup, width=entry_width, font=font_size)
            entry_customer_phone.grid(row=2, column=1, **padding)
            entry_customer_phone.insert(0, invoice["customer_phone"])

            tk.Label(popup, text="Indirizzo Cliente:", font=font_size).grid(row=3, column=0, **padding)
            entry_customer_address = tk.Entry(popup, width=entry_width, font=font_size)
            entry_customer_address.grid(row=3, column=1, **padding)
            entry_customer_address.insert(0, invoice["customer_address"])

            tk.Label(popup, text="Partita IVA:", font=font_size).grid(row=6, column=0, **padding)
            entry_vat_number = tk.Entry(popup, width=entry_width, font=font_size)
            entry_vat_number.grid(row=6, column=1, **padding)
            entry_vat_number.insert(0, invoice["vat_number"])

            tk.Label(popup, text="Condizioni di Pagamento:", font=font_size).grid(row=11, column=0, **padding)
            entry_payment_condition = tk.Entry(popup, width=entry_width, font=font_size)
            entry_payment_condition.grid(row=11, column=1, **padding)
            entry_payment_condition.insert(0, invoice["payment_condition"])

            tk.Label(popup, text="Mittente:", font=font_size).grid(row=12, column=0, **padding)
            entry_sender_name = tk.Entry(popup, width=entry_width, font=font_size)
            entry_sender_name.grid(row=12, column=1, **padding)
            entry_sender_name.insert(0, invoice["sender_name"])



            tk.Label(popup, text="Servizio di Corriere:", font=font_size).grid(row=14, column=0, **padding)
            entry_courier_service = tk.Entry(popup, width=entry_width, font=font_size)
            entry_courier_service.grid(row=14, column=1, **padding)
            entry_courier_service.insert(0, invoice["courier_service"])

            tk.Label(popup, text="Destinatario:", font=font_size).grid(row=15, column=0, **padding)
            entry_recipient = tk.Entry(popup, width=entry_width, font=font_size)
            entry_recipient.grid(row=15, column=1, **padding)
            entry_recipient.insert(0, invoice["recipient"])

            tk.Label(popup, text="Quantità Totale:", font=font_size).grid(row=16, column=0, **padding)
            entry_total_quantity = tk.Entry(popup, width=entry_width, font=font_size)
            entry_total_quantity.grid(row=16, column=1, **padding)
            entry_total_quantity.insert(0, invoice["total_quantity"])

            tk.Label(popup, text="IVA:", font=font_size).grid(row=17, column=0, **padding)
            entry_iva_amount = tk.Entry(popup, width=entry_width, font=font_size)
            entry_iva_amount.grid(row=17, column=1, **padding)
            entry_iva_amount.insert(0, invoice["iva_amount"])

            tk.Label(popup, text="Importo Totale:", font=font_size).grid(row=18, column=0, **padding)
            entry_total_amount = tk.Entry(popup, width=entry_width, font=font_size)
            entry_total_amount.grid(row=18, column=1, **padding)
            entry_total_amount.insert(0, invoice["total_amount"])

            tk.Label(popup, text="Totale Fattura EURO:", font=font_size).grid(row=19, column=0, **padding)
            entry_total_invoice_euro = tk.Entry(popup, width=entry_width, font=font_size)
            entry_total_invoice_euro.grid(row=19, column=1, **padding)
            entry_total_invoice_euro.insert(0, invoice["total_invoice_euro"])

            # Create headers for product fields
            tk.Label(popup, text="Articolo", font=font_size).grid(row=0, column=2, **padding)
            tk.Label(popup, text="Descrizione", font=font_size).grid(row=0, column=3, **padding)
            tk.Label(popup, text="Quantità", font=font_size).grid(row=0, column=4, **padding)
            tk.Label(popup, text="Prezzo", font=font_size).grid(row=0, column=5, **padding)
            tk.Label(popup, text="Sconto", font=font_size).grid(row=0, column=6, **padding)
            tk.Label(popup, text="Importo", font=font_size).grid(row=0, column=7, **padding)

            # Create entries for each product in a row
            product_entries = []
            for i, product in enumerate(products):
                entry_article = tk.Entry(popup, width=10, font=font_size)
                entry_article.grid(row=1 + i, column=2, **padding)
                entry_article.insert(0, product["article"])

                entry_description = tk.Entry(popup, width=20, font=font_size)
                entry_description.grid(row=1 + i, column=3, **padding)
                entry_description.insert(0, product["product_description"])

                entry_quantity = tk.Entry(popup, width=10, font=font_size)
                entry_quantity.grid(row=1 + i, column=4, **padding)
                entry_quantity.insert(0, product["product_quantity"])

                entry_price = tk.Entry(popup, width=10, font=font_size)
                entry_price.grid(row=1 + i, column=5, **padding)
                entry_price.insert(0, product["product_price"])

                entry_discount = tk.Entry(popup, width=10, font=font_size)
                entry_discount.grid(row=1 + i, column=6, **padding)
                entry_discount.insert(0, product["product_discount"])

                entry_amount = tk.Entry(popup, width=10, font=font_size)
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

            # Add save changes button at the bottom
            tk.Button(popup, text="Salva modifiche e conferma", command=save_changes, font=font_size).grid(row=22,
                                                                                                           columnspan=2,
                                                                                                           pady=30)

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
        pdf.thank_you_details(invoice)# Anche qui potrebbero esserci modifiche per riflettere che è una bolla di non venduto

        # Salva il PDF nel percorso scelto
        choose_save_path = lambda: None  # Implementa una logica simile a quella esistente per salvare il PDF
        choose_save_path()

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


    class PDFReturn(FPDF):
        def header(self):

            # Aggiungi il logo in alto a sinistra
            self.image('C:/PROGETTO/myapp/resources/LogoCINCOTTI.jpg', 8, 2, 77, 44,
                       'JPG')  # Modifica il percorso e le dimensioni

            # Aggiungi l'immagine in alto a destra
            self.image('C:/PROGETTO/myapp/resources/Logojpeg.jpg', 120, 8, 77, 33,
                       'JPG')  # Modifica il percorso e le dimensioni

            self.ln(35)

        def footer(self):
            # Aggiungi l'immagine in basso al centro
            self.set_y(-40)  # Posiziona a 30 mm dal fondo della pagina
            self.image('C:/PROGETTO/myapp/resources/LOGOMOZZABELLAECINCOTTI.jpg', 75, self.get_y(), 70, 40,
                       'JPG')  # Modifica il percorso e le dimensioni

        def draw_table(self, data, col_widths, headers=None, bold_headers=False):
            if headers:
                self.set_font('Arial', 'B', 10) if bold_headers else self.set_font('Arial', '', 10)
                for header, width in zip(headers, col_widths):
                    self.cell(width, 8, header, 1, 0, 'C')
                self.ln()

            self.set_font('Arial', '', 10)

            for row in data:
                row_heights = [self.calculate_cell_height(datum, width) for datum, width in zip(row, col_widths)]
                max_row_height = max(row_heights)

                x_start = self.get_x()
                y_start = self.get_y()
                for datum, width in zip(row, col_widths):
                    self.multi_cell(width, 6, datum if datum.strip() != "" else "-", 1, 'L', False)
                    self.set_xy(x_start + width, y_start)
                    x_start += width
                self.ln(max_row_height)  # Move down to start the next row

        def calculate_cell_height(self, text, width):
            """ Calculate the necessary cell height for the text based on the column width. """
            self.set_font('Arial', '', 10)
            num_lines = max(1, self.get_string_width(text) / width)  # Ensure at least one line
            return 6 * (text.count('\n') + num_lines)  # Line height times the number of lines

        def invoice_header(self, invoice):
            self.set_font('Arial', '', 10)
            data = [
                f"Document: Bolla di reso", f"n. {invoice['number']}", f"Data: {invoice['Date_1']}"
            ]
            col_widths = [70, 40, 70]  # Regola le larghezze delle colonne come necessario
            self.draw_table([data], col_widths)

        def customer_details(self, invoice):
            data = [
                ["Goods destination:\n" + invoice["customer_phone"], "Customer:\n" + invoice["customer_address"]],
            ]
            col_widths = [70, 110]  # Regola le larghezze delle colonne come necessario
            self.draw_table(data, col_widths, bold_headers=True)

        def product_table(self, products):
            headers = ["Article", "Description", "Quantity", "Price", "Discount", "Amount"]
            data = [
                [product['article'], product['product_description'], str(product['product_quantity']),
                 str(product['product_price']), str(product['product_discount']), str(product['product_amount'])]
                for product in products
            ]
            col_widths = [20, 70, 20, 20, 20, 30]
            self.set_font('Arial', 'B', 10)
            self.cell(0, 8, 'Product Details', 0, 1, 'L')
            self.draw_table(data, col_widths, headers, bold_headers=True)

        def total_details(self, invoice):
            data = [
                ["Total Quantity:\n" + str(invoice["total_quantity"]), "IVA:\n" + " ", "Mittente:\n" + invoice["sender_name"]],
                ["Causale trasporto:\n" + "Reso", "Trasporto a mezzo:\n" + "Vettore ", "Destinatario:\n" + invoice["recipient"]],
                ["Imponibile:\n" + str(invoice["total_amount"]), "Importo IVA:\n" + str(invoice["iva_amount"]),
                 "Totale Fattura EURO:\n" + str(invoice["total_invoice_euro"])],
            ]
            col_widths = [60, 60, 60]
            self.set_font('Arial', 'B', 10)
            self.cell(0, 8, 'Total Details', 0, 1, 'L')
            self.draw_table(data, col_widths, bold_headers=True)

    def generate_return_pdf(order):
        invoice_number = order[0]
        invoice = fetch_invoice_data(invoice_number)
        products = fetch_invoice_products(invoice_number)
        if not invoice:
            messagebox.showerror("Errore", "Dati della bolla di reso non trovati.")
            return

        # Popup window to edit and confirm invoice data
        def edit_and_confirm():
            def save_changes():
                # Update invoice data from the entry fields
                invoice["number"] = entry_number.get()
                invoice["Date_1"] = entry_date.get()
                invoice["customer_phone"] = entry_customer_phone.get()
                invoice["customer_address"] = entry_customer_address.get()
                invoice["recipient"] = entry_recipient.get()
                invoice["total_quantity"] = entry_total_quantity.get()
                invoice["total_amount"] = entry_total_amount.get()
                invoice["total_invoice_euro"] = entry_total_invoice_euro.get()

                # Close the popup window after saving changes
                popup.destroy()

                # Open a separate window to choose save path
                choose_save_path()

            # Ottiene la data corrente e la formatta come YYYYMMDD
            current_date = datetime.now().strftime("%Y%m%d")
            filename = f"Bolla_Reso_{current_date}"

            def choose_save_path():
                save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], initialfile=filename)
                if save_path:
                    pdf = PDFReturn()
                    pdf.add_page()
                    pdf.invoice_header(invoice)
                    pdf.customer_details(invoice)
                    pdf.product_table(products)
                    pdf.total_details(invoice)
                    pdf.output(save_path)
                    messagebox.showinfo("Successo", f"Fattura salvata come {os.path.basename(save_path)}")
                else:
                    messagebox.showwarning("Salvataggio Annullato", "Il salvataggio della fattura è stato annullato.")

            # Create the popup window
            popup = tk.Toplevel()
            popup.title("Modifica i dettagli della fattura")
            popup.geometry("800x600")  # Set the size of the popup window
            popup.resizable(True, True)  # Prevent resizing for consistent layout

            # Add padding and spacing between elements
            padding = {'padx': 10, 'pady': 5}
            # Set the width of entry fields and the font size
            entry_width = 40
            font_size = ("Arial", 14)  # Font family Arial, size 14

            # Create and grid labels and entries for each invoice field with larger font
            tk.Label(popup, text="Numero:", font=font_size).grid(row=0, column=0, **padding)
            entry_number = tk.Entry(popup, width=entry_width, font=font_size)
            entry_number.grid(row=0, column=1, **padding)
            entry_number.insert(0, invoice["number"])

            tk.Label(popup, text="Data:", font=font_size).grid(row=1, column=0, **padding)
            entry_date = tk.Entry(popup, width=entry_width, font=font_size)
            entry_date.grid(row=1, column=1, **padding)
            entry_date.insert(0, invoice["Date_1"])

            tk.Label(popup, text="Telefono Cliente:", font=font_size).grid(row=2, column=0, **padding)
            entry_customer_phone = tk.Entry(popup, width=entry_width, font=font_size)
            entry_customer_phone.grid(row=2, column=1, **padding)
            entry_customer_phone.insert(0, invoice["customer_phone"])

            tk.Label(popup, text="Indirizzo Cliente:", font=font_size).grid(row=3, column=0, **padding)
            entry_customer_address = tk.Entry(popup, width=entry_width, font=font_size)
            entry_customer_address.grid(row=3, column=1, **padding)
            entry_customer_address.insert(0, invoice["customer_address"])

            tk.Label(popup, text="Mittente:", font=font_size).grid(row=12, column=0, **padding)
            entry_sender_name = tk.Entry(popup, width=entry_width, font=font_size)
            entry_sender_name.grid(row=12, column=1, **padding)
            entry_sender_name.insert(0, invoice["sender_name"])

            tk.Label(popup, text="Destinatario:", font=font_size).grid(row=15, column=0, **padding)
            entry_recipient = tk.Entry(popup, width=entry_width, font=font_size)
            entry_recipient.grid(row=15, column=1, **padding)
            entry_recipient.insert(0, invoice["recipient"])

            tk.Label(popup, text="Quantità Totale:", font=font_size).grid(row=16, column=0, **padding)
            entry_total_quantity = tk.Entry(popup, width=entry_width, font=font_size)
            entry_total_quantity.grid(row=16, column=1, **padding)
            entry_total_quantity.insert(0, invoice["total_quantity"])

            tk.Label(popup, text="Importo IVA:", font=font_size).grid(row=17, column=0, **padding)
            entry_iva_amount = tk.Entry(popup, width=entry_width, font=font_size)
            entry_iva_amount.grid(row=17, column=1, **padding)
            entry_iva_amount.insert(0, invoice["iva_amount"])

            tk.Label(popup, text="Imponibile:", font=font_size).grid(row=18, column=0, **padding)
            entry_total_amount = tk.Entry(popup, width=entry_width, font=font_size)
            entry_total_amount.grid(row=18, column=1, **padding)
            entry_total_amount.insert(0, invoice["total_amount"])

            tk.Label(popup, text="Totale Fattura EURO:", font=font_size).grid(row=19, column=0, **padding)
            entry_total_invoice_euro = tk.Entry(popup, width=entry_width, font=font_size)
            entry_total_invoice_euro.grid(row=19, column=1, **padding)
            entry_total_invoice_euro.insert(0, invoice["total_invoice_euro"])

            # Add save changes button at the bottom
            tk.Button(popup, text="Salva modifiche e conferma", command=save_changes, font=font_size).grid(row=22, columnspan=2,
                                                                                           pady=30)

        edit_and_confirm()
        # Continue to generate the PDF after the popup is closed
        pdf = PDFReturn()
        pdf.add_page()
        pdf.invoice_header(invoice)
        pdf.customer_details(invoice)
        pdf.product_table(products)
        pdf.total_details(invoice)

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
    button_return = ctk.CTkButton(parent_frame, text="Annulla operazione", command=show_invoice_form)
    button_return.pack(side="left", padx=10, pady=20)

