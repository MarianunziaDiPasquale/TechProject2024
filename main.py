import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from dashboards.dashboard_magazzino_ap import show_dashboard1
from dashboards.dashboard_categorie import show_dashboard2
from dashboards.dashboard_clienti import show_dashboard3
from dashboards.dashboard_agenti import show_dashboard4
from dashboards.dashboard_vettori import show_dashboard5
from dashboards.dashboard_fornitori import show_dashboard6
from dashboards.dashboard_moduli import show_dashboard7
from dashboards.dashboard_storico_ordini import show_dashboard8
from dashboards.dashboard_consiglio import show_dashboard9
from side_panel import create_side_panel_buttons

# Imposta la modalità di customtkinter e il tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def add_title_and_frame(parent_frame, title, on_close_callback, on_extract_callback):
    """Helper function to create a labeled frame with close and extract buttons."""
    title_bar = ctk.CTkFrame(parent_frame, corner_radius=0)
    title_bar.pack(fill="x")

    label = ctk.CTkLabel(title_bar, text=title, font=('Arial', 15, 'bold'))
    label.pack(side="left", padx=10, pady=5)

    extract_button = ctk.CTkButton(title_bar, text="↗", width=25, command=on_extract_callback)
    extract_button.pack(side="right", padx=10, pady=5)

    close_button = ctk.CTkButton(title_bar, text="✖", width=25, command=on_close_callback)
    close_button.pack(side="right", padx=10, pady=5)

    dashboard_frame = ctk.CTkFrame(parent_frame, corner_radius=5)
    dashboard_frame.pack(fill="both", expand=True)

    return dashboard_frame

def open_dashboard_popup(title, content_func):
    """Create a new popup window for the dashboard."""
    popup = tk.Toplevel()
    popup.title(title)

    # Center the popup
    window_width = 800
    window_height = 600
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    popup.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    dashboard_frame = ctk.CTkFrame(popup, corner_radius=5)
    dashboard_frame.pack(fill="both", expand=True)

    content_func(dashboard_frame)  # Load the content into the popup

def update_dashboard():
    """Update the main frame to show multiple dashboards."""
    # Rimuovi tutti i frame dal PanedWindow ma senza distruggerli
    for pane in main_frame.panes():
        main_frame.forget(pane)

    if not open_dashboards:
        main_frame.place_forget()  # Nasconde il PanedWindow se non ci sono dashboard
        background_canvas.pack(fill="both", expand=True)  # Mostra il canvas di sfondo
        #hide_frames()  # Nasconde i pulsanti se non ci sono dashboard
    else:
        main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.98, relheight=0.90)  # Mostra il PanedWindow

        #show_buttons = True  # Controlla se mostrare i pulsanti superiori e inferiori

        for dashboard in open_dashboards:
            if dashboard in dashboard_frames:
                frame = dashboard_frames[dashboard]
            else:
                frame = ctk.CTkFrame(main_frame, corner_radius=5)
                dashboard_frames[dashboard] = frame  # Memorizza il frame nel dizionario

                def close_dashboard(dashboard_name=dashboard):
                    open_dashboards.remove(dashboard_name)
                    del dashboard_frames[dashboard_name]  # Rimuovi il frame dal dizionario
                    update_dashboard()

                def extract_dashboard(dashboard_name="dashboard"):
                    # Chiudi il frame nel PanedWindow e apri il popup
                    close_dashboard(dashboard_name)
                    if dashboard_name == "1":
                        open_dashboard_popup("Magazzino Andria-Parigi", show_dashboard1)
                    elif dashboard_name == "2":
                        open_dashboard_popup("Categorie", show_dashboard2)
                    elif dashboard_name == "3":
                        open_dashboard_popup("Clienti", show_dashboard3)
                    elif dashboard_name == "4":
                        open_dashboard_popup("Agenti", show_dashboard4)
                    elif dashboard_name == "5":
                        open_dashboard_popup("Vettori", show_dashboard5)
                    elif dashboard_name == "6":
                        open_dashboard_popup("Fornitori", show_dashboard6)
                    elif dashboard_name == "7":
                        open_dashboard_popup("Inserimento Moduli", show_dashboard7)
                    elif dashboard_name == "8":
                        open_dashboard_popup("Storico Ordini", show_dashboard8)
                    elif dashboard_name == "9":
                        open_dashboard_popup("Consiglio Ordini", show_dashboard9)

                # Mapping buttons to the dashboard functions

                if dashboard == "1":
                    dashboard_frame = add_title_and_frame(frame, "Magazzino Andria-Parigi",
                                                          lambda: close_dashboard("1"), lambda: extract_dashboard("1"))
                    show_dashboard1(dashboard_frame)
                elif dashboard == "2":
                    dashboard_frame = add_title_and_frame(frame, "Categorie", lambda: close_dashboard("2"),
                                                          lambda: extract_dashboard("2"))
                    show_dashboard2(dashboard_frame)
                elif dashboard == "3":
                    dashboard_frame = add_title_and_frame(frame, "Clienti", lambda: close_dashboard("3"),
                                                          lambda: extract_dashboard("3"))
                    show_dashboard3(dashboard_frame)
                elif dashboard == "4":
                    dashboard_frame = add_title_and_frame(frame, "Agenti", lambda: close_dashboard("4"),
                                                          lambda: extract_dashboard("4"))
                    show_dashboard4(dashboard_frame)
                elif dashboard == "5":
                    dashboard_frame = add_title_and_frame(frame, "Vettori", lambda: close_dashboard("5"),
                                                          lambda: extract_dashboard("5"))
                    show_dashboard5(dashboard_frame)
                elif dashboard == "6":
                    dashboard_frame = add_title_and_frame(frame, "Fornitori", lambda: close_dashboard("6"),
                                                          lambda: extract_dashboard("6"))
                    show_dashboard6(dashboard_frame)
                elif dashboard == "7":
                    dashboard_frame = add_title_and_frame(frame, "Inserimento Moduli", lambda: close_dashboard("7"),
                                                          lambda: extract_dashboard("7"))
                    show_dashboard7(dashboard_frame)
                elif dashboard == "8":
                    dashboard_frame = add_title_and_frame(frame, "Storico Ordini", lambda: close_dashboard("8"),
                                                          lambda: extract_dashboard("8"))
                    show_dashboard8(dashboard_frame)
                elif dashboard == "9":
                    dashboard_frame = add_title_and_frame(frame, "Consiglio Ordini", lambda: close_dashboard("9"),
                                                          lambda: extract_dashboard("9"))
                    show_dashboard9(dashboard_frame)

            main_frame.add(frame)  # Aggiungi frame al PanedWindow senza ricrearlo

        """
        if show_buttons:
            show_dashboard_buttons()
        else:
            hide_frames()
        """

# Inizializza un dizionario per tenere traccia dei frame delle dashboard
dashboard_frames = {}

def toggle_side_panel():
    if side_panel.winfo_ismapped():
        side_panel.place_forget()
        toggle_button.configure(text="☰")
    else:
        side_panel.place(relx=0.5, rely=0, anchor="n", relwidth=1)
        toggle_button.configure(text="✖")

def show_dashboard_buttons():
    bottom_frame.place(relx=0.5, rely=0.999, anchor="s")
    """
    button_add_client.pack(side='left', padx=10, pady=5)
    button_add_product.pack(side='left', padx=10, pady=5)
    button_add_supplier.pack(side='left', padx=10, pady=5)

    button_remove_client.pack(side='left', padx=10, pady=5)
    button_remove_product.pack(side='left', padx=10, pady=5)
    button_remove_supplier.pack(side='left', padx=10, pady=5)
    """

def hide_all_buttons():
    for widget in bottom_frame.winfo_children():
        widget.pack_forget()

def hide_frames():
    bottom_frame.place_forget()

def open_settings_popup():
    popup = tk.Toplevel()
    popup.title("Impostazioni")

    # Center the popup
    window_width = 400
    window_height = 200
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    popup.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    label = tk.Label(popup, text="Scegli il tema grafico", font=('Arial', 14))
    label.pack(pady=10)

    def change_appearance_mode(new_mode):
        ctk.set_appearance_mode(new_mode)
        popup.destroy()

    light_mode_button = tk.Button(popup, text="Chiaro", command=lambda: change_appearance_mode("light"), font=('Arial', 12))
    light_mode_button.pack(pady=5)

    dark_mode_button = tk.Button(popup, text="Scuro", command=lambda: change_appearance_mode("dark"), font=('Arial', 12))
    dark_mode_button.pack(pady=5)

def main():
    global main_frame, open_dashboards, side_panel, toggle_button, bottom_frame, background_canvas
    #global button_add_client, button_remove_client, button_add_product, button_remove_product, button_add_supplier, button_remove_supplier

    root = ctk.CTk()
    root.title("AppTechProject")
    root.geometry("1800x1200")


    # Carica l'immagine di sfondo
    background_image = Image.open("resources/Geometry_Texture.jpg")
    background_image = background_image.resize((2000, 1300), Image.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)

    # Canvas per l'immagine di sfondo
    background_canvas = tk.Canvas(root, width=1800, height=1200)
    background_canvas.pack(fill="both", expand=True)
    background_canvas.create_image(0, 0, image=background_photo, anchor="nw")

    # Usa PanedWindow per il frame principale
    main_frame = tk.PanedWindow(root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, showhandle=True)
    main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.98, relheight=0.87)

    # Pannello orizzontale per le dashboard (in alto)
    side_panel = ctk.CTkFrame(root, height=100, corner_radius=5)
    side_panel.place(relx=0.5, rely=0, anchor="n", relwidth=1)

    # Pulsante di toggle all'esterno del pannello orizzontale, allineato con esso
    toggle_button = ctk.CTkButton(root, text="☰", command=toggle_side_panel, corner_radius=5 , font=('Arial', 11), height=15, width=40)
    toggle_button.place(relx=0.01, rely=0.008, anchor="nw")

    # Crea i pulsanti nel pannello orizzontale (disposti uno accanto all'altro)
    create_side_panel_buttons(side_panel, toggle_side_panel, lambda dashboards: add_dashboards(dashboards))

    # Frame per i pulsanti inferiori
    #bottom_frame = ctk.CTkFrame(root, corner_radius=5)

    #button_add_client, button_add_product, button_add_supplier, button_remove_client, button_remove_product, button_remove_supplier = create_dashboard_buttons(bottom_frame)

    settings_button = tk.Button(root, text="Impostazioni", command=open_settings_popup, font=('Arial', 10))
    settings_button.place(relx=0.99, rely=0.96, anchor="ne")

    #hide_all_buttons()
    #hide_frames()
    main_frame.place_forget()  # Nasconde il PanedWindow se non ci sono dashboard
    background_canvas.pack(fill="both", expand=True)  # Mostra il canvas di sfondo

    # Inizializza l'elenco per tenere traccia delle dashboard aperte
    open_dashboards = []

    root.mainloop()

def add_dashboards(dashboards):
    # Questa funzione assume che "dashboards" sia una lista di dashboard da aggiungere
    for dashboard in dashboards:
        if dashboard not in open_dashboards:
            if len(open_dashboards) >= 3:  # Controlla se ci sono già 3 dashboard aperte
                oldest_dashboard = open_dashboards.pop(0)  # Rimuove la più vecchia dalla lista
                del dashboard_frames[oldest_dashboard]  # Rimuove il frame dalla memoria
            open_dashboards.append(dashboard)  # Aggiungi la nuova dashboard alla lista
    update_dashboard()

if __name__ == "__main__":
    main()
