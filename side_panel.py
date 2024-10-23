import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk

def load_icons():
    icon1 = Image.open("resources/home.png").resize((20, 20), Image.LANCZOS)
    icon2 = Image.open("resources/shopping-cart.png").resize((20, 20), Image.LANCZOS)
    icon3 = Image.open("resources/users-alt.png").resize((20, 20), Image.LANCZOS)
    icon4 = Image.open("resources/briefcase.png").resize((20, 20), Image.LANCZOS)
    icon5 = Image.open("resources/truck-side.png").resize((20, 20), Image.LANCZOS)
    icon6 = Image.open("resources/boxes.png").resize((20, 20), Image.LANCZOS)
    icon7 = Image.open("resources/apps.png").resize((20, 20), Image.LANCZOS)
    icon8 = Image.open("resources/money-check-edit.png").resize((20, 20), Image.LANCZOS)
    icon9 = Image.open("resources/lightbulb-on.png").resize((20, 20), Image.LANCZOS)
    icon10 = Image.open("resources/insert-credit-card.png").resize((20, 20), Image.LANCZOS)

    icon1 = ImageTk.PhotoImage(icon1)
    icon2 = ImageTk.PhotoImage(icon2)
    icon3 = ImageTk.PhotoImage(icon3)
    icon4 = ImageTk.PhotoImage(icon4)
    icon5 = ImageTk.PhotoImage(icon5)
    icon6 = ImageTk.PhotoImage(icon6)
    icon7 = ImageTk.PhotoImage(icon7)
    icon8 = ImageTk.PhotoImage(icon8)
    icon9 = ImageTk.PhotoImage(icon9)
    icon10 = ImageTk.PhotoImage(icon10)

    return icon1, icon2, icon3, icon4, icon5, icon6, icon7, icon8, icon9, icon10

def create_side_panel_buttons(side_panel, toggle_side_panel, update_dashboard):
    icon1, icon2, icon3, icon4, icon5, icon6, icon7, icon8, icon9, icon10 = load_icons()

    button_width = 150  # Set a fixed width for all buttons
    button_padding_x = 7 # Set the padding for both sides of the button

    button_dashboard1 = ctk.CTkButton(side_panel, text="Magazzino Andria-Parigi", image=icon1, compound="left",
                                      command=lambda: [update_dashboard("1")],
                                      corner_radius=5, anchor="w",font=('Arial', 11), height=15, width=130)
    button_dashboard1.pack(side="left",pady=4, padx=(70, 10), fill="x")

    button_dashboard2 = ctk.CTkButton(side_panel, text="Categorie", image=icon2, compound="left",
                                      command=lambda: [update_dashboard("2")],
                                      corner_radius=5, anchor="w",font=('Arial', 11), height=15, width=90)
    button_dashboard2.pack(side="left",pady=4, padx=button_padding_x, fill="x")

    button_dashboard3 = ctk.CTkButton(side_panel, text="Clienti", image=icon3, compound="left",
                                      command=lambda: [update_dashboard("3")],
                                      corner_radius=5, anchor="w",font=('Arial', 11), height=15, width=90)
    button_dashboard3.pack(side="left",pady=4, padx=button_padding_x, fill="x")

    button_dashboard4 = ctk.CTkButton(side_panel, text="Agenti", image=icon4, compound="left",
                                      command=lambda: [update_dashboard("4")],
                                      corner_radius=5, anchor="w", font=('Arial', 11), height=15, width=90)
    button_dashboard4.pack(side="left", pady=4, padx=button_padding_x, fill="x")

    button_dashboard5 = ctk.CTkButton(side_panel, text="Vettori", image=icon5, compound="left",
                                      command=lambda: [update_dashboard("5")],
                                      corner_radius=5, anchor="w", font=('Arial', 11), height=15, width=90)
    button_dashboard5.pack(side="left", pady=4, padx=button_padding_x, fill="x")

    button_dashboard6 = ctk.CTkButton(side_panel, text="Fornitori", image=icon6, compound="left",
                                      command=lambda: [update_dashboard("6")],
                                      corner_radius=5, anchor="w", font=('Arial', 11), height=15, width=90)
    button_dashboard6.pack(side="left", pady=4, padx=button_padding_x, fill="x")

    button_dashboard10 = ctk.CTkButton(side_panel, text="Condizioni-Metodi Pay", image=icon10, compound="left",
                                      command=lambda: [update_dashboard("A")],
                                      corner_radius=5, anchor="w", font=('Arial', 11), height=15, width=90)
    button_dashboard10.pack(side="left", pady=4, padx=button_padding_x, fill="x")

    button_dashboard7 = ctk.CTkButton(side_panel, text="Inserimento Moduli", image=icon7, compound="left",
                                      command=lambda: [update_dashboard("7")],
                                      corner_radius=5, anchor="w",font=('Arial', 11), height=15, width=90)
    button_dashboard7.pack(side="left",pady=4, padx=button_padding_x, fill="x")

    button_dashboard8 = ctk.CTkButton(side_panel, text="Storico Ordini", image=icon8, compound="left",
                                      command=lambda: [update_dashboard("8")],
                                      corner_radius=5,anchor="w",font=('Arial', 11), height=15, width=90)
    button_dashboard8.pack(side="left",pady=4, padx=button_padding_x, fill="x")

    button_dashboard9 = ctk.CTkButton(side_panel, text="Consiglio Ordini", image=icon9, compound="left",
                                      command=lambda: [update_dashboard("9")],
                                      corner_radius=5, anchor="w",font=('Arial', 11), height=15, width=90)
    button_dashboard9.pack(side="left",pady=4, padx=button_padding_x, fill="x")
