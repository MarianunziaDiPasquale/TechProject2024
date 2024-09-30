import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog

def show_dashboard6(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    dashboard6_frame = ctk.CTkFrame(parent_frame, corner_radius=5)
    dashboard6_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Create a frame for the notepad
    notepad_frame = ctk.CTkFrame(dashboard6_frame, corner_radius=5)
    notepad_frame.pack(pady=10, padx=10, fill="x", expand=False)

    notepad_label = ctk.CTkLabel(notepad_frame, text="Blocco Note:", font=('Arial', 14, 'bold'))
    notepad_label.pack(pady=5)

    notepad_text = tk.Text(notepad_frame, wrap="word", font=('Arial', 14), height=10)  # Adjust height for a smaller notepad
    notepad_text.pack(pady=10, padx=10, fill="x", expand=False)

    # Save the content of the notepad to a file
    def save_notepad():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(notepad_text.get("1.0", tk.END))

    # Load the content of the notepad from a file
    def load_notepad():
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                notepad_text.delete("1.0", tk.END)
                notepad_text.insert(tk.END, file.read())

    # Add save and load buttons
    button_frame = ctk.CTkFrame(notepad_frame, corner_radius=5)
    button_frame.pack(pady=5)

    save_button = ctk.CTkButton(button_frame, text="Salva", command=save_notepad)
    save_button.pack(side="left", padx=5)

    load_button = ctk.CTkButton(button_frame, text="Carica", command=load_notepad)
    load_button.pack(side="left", padx=5)

    # Create a frame for the checklist
    checklist_frame = ctk.CTkFrame(dashboard6_frame, corner_radius=5)
    checklist_frame.pack_propagate(False)
    checklist_frame.pack(pady=10, padx=10, fill="both", expand=True)

    checklist_label = ctk.CTkLabel(checklist_frame, text="Checklist:", font=('Arial', 14, 'bold'))
    checklist_label.pack(pady=5)

    # Create a list to hold the state of the checkboxes
    checklist_items = []

    def add_checklist_item():
        entry_text = checklist_entry.get()
        if entry_text:
            var = tk.IntVar()
            item_frame = tk.Frame(checklist_frame)
            item_frame.pack(anchor='w', pady=2, padx=10, fill='x')

            checkbutton = tk.Checkbutton(item_frame, text=entry_text, variable=var, font=('Arial', 14))
            checkbutton.pack(side='left')

            remove_button = tk.Button(item_frame, text="Rimuovi", command=lambda: remove_checklist_item(item_frame))
            remove_button.pack(side='right')

            checklist_items.append((entry_text, var, item_frame))
            checklist_entry.delete(0, tk.END)

    def remove_checklist_item(item_frame):
        for item in checklist_items:
            if item[2] == item_frame:
                checklist_items.remove(item)
                item_frame.destroy()
                break

    checklist_entry = tk.Entry(checklist_frame, font=('Arial', 14))
    checklist_entry.pack(pady=5, padx=10, fill='x')

    add_button = ctk.CTkButton(checklist_frame, text="Aggiungi alla checklist", command=add_checklist_item)
    add_button.pack(pady=5)