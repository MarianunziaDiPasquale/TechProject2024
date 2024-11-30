import customtkinter as ctk
from tkinter import Toplevel, Listbox, Scrollbar, Entry, Button, Label, messagebox
import tkinter as tk

dashboard_font_size = 14

# Simuliamo le due tabelle con delle liste (puoi sostituire con le tue query al database)
table1_data = [{"id": 1, "nome": "Prelevement le 17 mois suivant"}, {"id": 2, "nome": "Prelevement le 20 mois suivant"}]
table2_data = [{"id": 1, "nome": "MP20 SEPA Direct Debit CORE"}, {"id": 2, "nome": "MP05"}]


# Funzione per mostrare la dashboard con le due liste
def show_dashboard10(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()

        parent_frame_color = parent_frame.cget("fg_color")

    def open_font_size_popup():
        """Open a popup to choose the font size and reload the dashboard with the new size."""
        popup = tk.Toplevel()
        popup.title("Scegli la dimensione del font")
        popup.geometry("500x250")
        popup.transient()  # Make it modal

        # Label for font size selection
        label = tk.Label(popup, text="Seleziona la dimensione del font:", font=("Arial", dashboard_font_size))
        label.pack(pady=10)

        # Scale widget to select font size
        font_size_var = tk.IntVar(value=dashboard_font_size)
        # Label to display the current slider value on top of the slider handle
        value_display = ctk.CTkLabel(popup, text=str(dashboard_font_size), font=("Arial", dashboard_font_size))
        value_display.place(relx=0.5, rely=0.35, anchor="center")  # Initial position
        # CTkSlider to select font size with inverted color appearance
        slider_min = 10
        slider_max = 30
        font_slider = ctk.CTkSlider(
            popup,
            from_=10,
            to=30,
            number_of_steps=20,
            fg_color="white",
            progress_color= "blue",
            command=lambda value: update_slider_value(value) # Sync slider value to font_size_var
        )
        font_slider.set(dashboard_font_size)  # Set initial slider position
        font_slider.pack(pady=10)

        def update_slider_value(value):
            """Update the label text and position to follow the slider handle."""
            font_size_var.set(int(value))  # Update the IntVar with the new slider value
            value_display.configure(text=str(int(value)))  # Update the display label text
            # Position the display label above the slider handle
            slider_pos = font_slider.get()
            display_x = 20 + (slider_pos - slider_min) / (slider_max - slider_min) * 240
            value_display.place(x=display_x, y=60)

        def apply_font_size():
            global dashboard_font_size
            dashboard_font_size = int(font_slider.get())
            popup.destroy()
            # Clear the existing dashboard and reload it with the new font size
            for widget in parent_frame.winfo_children():
                widget.destroy()  # Remove all existing widgets from parent_frame
            show_dashboard10(parent_frame)

        # Button to confirm font size selection
        apply_button = ctk.CTkButton(popup, text="Applica", font=("Arial", dashboard_font_size), command=apply_font_size)
        apply_button.pack(pady=10)

    # Crea due frame per contenere le liste
    frame_table1 = ctk.CTkFrame(parent_frame, corner_radius=5)
    frame_table1.pack(side="left", padx=5, pady=10, fill="both", expand=True)

    frame_table2 = ctk.CTkFrame(parent_frame, corner_radius=5)
    frame_table2.pack(side="right", padx=5, pady=10, fill="both", expand=True)

    # Etichette per le due tabelle
    label_table1 = ctk.CTkLabel(frame_table1, text="Condizioni pagamento", font=('Arial', dashboard_font_size))
    label_table1.pack(pady=5)

    label_table2 = ctk.CTkLabel(frame_table2, text="Metodi pagamento", font=('Arial', dashboard_font_size))
    label_table2.pack(pady=5)

    # Crea le liste di elementi
    listbox_table1 = Listbox(frame_table1, font=('Arial', dashboard_font_size), height=10)
    listbox_table2 = Listbox(frame_table2, font=('Arial', dashboard_font_size), height=10)

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
    add_button_table1 = ctk.CTkButton(frame_table1, text="Aggiungi Elemento", font=("Arial", dashboard_font_size),
                                      command=lambda: open_add_popup("Tabella 1", table1_data, listbox_table1))
    add_button_table1.pack(side="left", padx=10)

    add_button_table2 = ctk.CTkButton(frame_table2, text="Aggiungi Elemento", font=("Arial", dashboard_font_size),
                                      command=lambda: open_add_popup("Tabella 2", table2_data, listbox_table2))
    add_button_table2.pack(side="left", padx=10)

    font_size_button = ctk.CTkButton(frame_table2, text="Cambia Dimensione Font", font=("Arial", dashboard_font_size),
                                     command=open_font_size_popup, corner_radius=5)
    font_size_button.pack(side="left", padx=10)

    font_size_button = ctk.CTkButton(frame_table1, text="Cambia Dimensione Font", font=("Arial", dashboard_font_size),
                                     command=open_font_size_popup, corner_radius=5)
    font_size_button.pack(side="left", padx=10)



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
    label_id = Label(popup, text="ID:", font=('Arial', dashboard_font_size), )
    label_id.pack(pady=5)
    entry_id = Entry(popup, font=('Arial', dashboard_font_size),  width=120, height=30)
    entry_id.pack(pady=5)
    entry_id.insert(0, item['id'])

    label_nome = Label(popup, text="Nome:", font=('Arial', dashboard_font_size))
    label_nome.pack(pady=5)
    entry_nome = Entry(popup, font=('Arial', dashboard_font_size),  width=120, height=30)
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
    save_button =ctk.CTkButton(popup, text="Salva Modifiche", command=save_changes, font=('Arial', dashboard_font_size), width=120, height=30)
    save_button.pack(pady=10)

    delete_button = ctk.CTkButton(popup, text="Elimina Elemento", command=delete_item, font=('Arial', dashboard_font_size),  width=120, height=30)
    delete_button.pack(pady=10)


# Funzione per aggiungere un nuovo elemento
def open_add_popup(tabella, data, listbox):
    popup = Toplevel()
    popup.title(f"Aggiungi Elemento a {tabella}")

    label_id = Label(popup, text="ID:", font=('Arial', dashboard_font_size))
    label_id.pack(pady=5)
    entry_id = Entry(popup, font=('Arial', dashboard_font_size))
    entry_id.pack(pady=5)

    label_nome = Label(popup, text="Nome:", font=('Arial', dashboard_font_size))
    label_nome.pack(pady=5)
    entry_nome = Entry(popup, font=('Arial', dashboard_font_size))
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

    add_button = ctk.CTkButton(popup, text="Aggiungi Elemento", command=add_new_item, font=('Arial', dashboard_font_size),  width=120, height=30)
    add_button.pack(pady=10)
