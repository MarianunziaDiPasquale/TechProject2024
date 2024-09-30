import customtkinter as ctk
import tkinter as ttk
from tkinter import simpledialog, messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


def generate_pdf(invoice_data):
    pdf_file = "fattura.pdf"
    c = canvas.Canvas(pdf_file, pagesize=A4)

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30 * mm, 275 * mm, "INVOICE")
    c.setFont("Helvetica", 12)
    c.drawString(30 * mm, 270 * mm, f"n° {invoice_data['invoice_number']}")
    c.drawString(100 * mm, 270 * mm, f"Date: {invoice_data['date']}")

    # Customer and goods destination
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30 * mm, 260 * mm, "Goods destination:")
    c.setFont("Helvetica", 10)
    c.drawString(30 * mm, 255 * mm, invoice_data['customer'])

    # Article details
    y_position = 240
    c.setFont("Helvetica-Bold", 10)
    c.drawString(30 * mm, y_position * mm, "ARTICLE")
    c.drawString(60 * mm, y_position * mm, "DESCRIPTION")
    c.drawString(120 * mm, y_position * mm, "CODE")
    c.drawString(140 * mm, y_position * mm, "QUANT.")
    c.drawString(160 * mm, y_position * mm, "PRICE")
    c.drawString(180 * mm, y_position * mm, "DISCOUNT")
    c.drawString(200 * mm, y_position * mm, "AMOUNT")

    y_position -= 10
    c.setFont("Helvetica", 10)
    for item in invoice_data['items']:
        c.drawString(30 * mm, y_position * mm, item['article'])
        c.drawString(60 * mm, y_position * mm, item['description'])
        c.drawString(120 * mm, y_position * mm, item['code'])
        c.drawString(140 * mm, y_position * mm, item['quantity'])
        c.drawString(160 * mm, y_position * mm, item['price'])
        c.drawString(180 * mm, y_position * mm, item['discount'])
        c.drawString(200 * mm, y_position * mm, item['amount'])
        y_position -= 10

    # Total Amount
    c.setFont("Helvetica-Bold", 12)
    c.drawString(160 * mm, (y_position - 10) * mm, f"Total Amount: {invoice_data['total_amount']}")

    c.save()
    messagebox.showinfo("PDF Generated", "The PDF has been generated successfully!")


def main():
    root = ctk.CTk()
    root.title("Invoice Generator")
    root.geometry("800x600")

    def add_item():
        article = simpledialog.askstring("Article", "Enter Article:")
        description = simpledialog.askstring("Description", "Enter Description:")
        code = simpledialog.askstring("Code", "Enter Code:")
        quantity = simpledialog.askstring("Quantity", "Enter Quantity:")
        price = simpledialog.askstring("Price", "Enter Price:")
        discount = simpledialog.askstring("Discount", "Enter Discount:")
        amount = simpledialog.askstring("Amount", "Enter Amount:")

        item = {
            'article': article,
            'description': description,
            'code': code,
            'quantity': quantity,
            'price': price,
            'discount': discount,
            'amount': amount
        }

        items.append(item)
        tree.insert("", tk.END, values=(article, description, code, quantity, price, discount, amount))

    def generate_invoice():
        invoice_number = simpledialog.askstring("Invoice Number", "Enter Invoice Number:")
        date = simpledialog.askstring("Date", "Enter Date:")
        customer = simpledialog.askstring("Customer", "Enter Customer:")
        total_amount = simpledialog.askstring("Total Amount", "Enter Total Amount:")

        invoice_data = {
            'invoice_number': invoice_number,
            'date': date,
            'customer': customer,
            'items': items,
            'total_amount': total_amount
        }

        generate_pdf(invoice_data)

    # Items list
    global items
    items = []

    # Main frame
    main_frame = ctk.CTkFrame(root, corner_radius=15)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Buttons
    button_frame = ctk.CTkFrame(main_frame, corner_radius=15)
    button_frame.pack(pady=10)

    add_item_button = ctk.CTkButton(button_frame, text="Add Item", command=add_item, corner_radius=15)
    add_item_button.grid(row=0, column=0, padx=10)

    generate_invoice_button = ctk.CTkButton(button_frame, text="Generate Invoice", command=generate_invoice,
                                            corner_radius=15)
    generate_invoice_button.grid(row=0, column=1, padx=10)

    # Treeview for items
    columns = ("Article", "Description", "Code", "Quantity", "Price", "Discount", "Amount")
    global tree
    tree = ttk.Treeview(main_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")
    tree.pack(pady=10, fill="both", expand=True)

    # Scrollbar
    scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    tree.pack(side="left", fill="both", expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()
