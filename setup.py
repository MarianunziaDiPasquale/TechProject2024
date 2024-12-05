'''
from cx_Freeze import setup, Executable

include_files = [
    ("resources/document.png", "resources/"),
    ("resources/edit.png", "resources/"),
    ("resources/home.png", "resources/"),
    ("resources/home_white.png", "resources/"),
    ("resources/insert-credit-card.png", "resources/"),
    ("resources/insert-credit-card_white.png", "resources/"),
    ("resources/lightbulb-on.png", "resources/"),
    ("resources/lightbulb-on_white.png", "resources/"),
    ("resources/money-check-edit.png", "resources/"),
    ("resources/money-check-edit_white.png", "resources/"),
    ("resources/shopping-cart.png", "resources/"),
    ("resources/shopping-cart_white.png", "resources/"),
    ("resources/truck-side.png", "resources/"),
    ("resources/truck-side_white.png", "resources/"),
    ("resources/users-alt.png", "resources/"),
    ("resources/users-alt_white.png", "resources/"),
    ("resources/create_table_insert.py", "resources/"),
    ("resources/Andria_data.xlsx", "resources/"),
    ("resources/requirements.txt", "resources/"),
    ("resources/geometric.jpg", "resources/"),
    ("resources/Geometry_Texture.jpg", "resources/"),
    ("resources/LogoCINCOTTI.jpg", "resources/"),
    ("resources/LOGOjpeg.jpg", "resources/"),
    ("resources/LOGOMOZZABELLAECINCOTTI SRLS.jpg", "resources/"),
    ("resources/LOGOMOZZABELLAECINCOTTI.jpg", "resources/"),
    ("resources/GhostTrain.json", "resources/"),
    ("resources/A_professional_sleek_abstract_background_16_9.png", "resources/"),
    ("resources/apps.png", "resources/"),
    ("resources/apps_white.png", "resources/"),
    ("resources/boxes.png", "resources/"),
    ("resources/boxes_white.png", "resources/"),
    ("resources/briefcase.png", "resources/"),
    ("resources/briefcase_white.png", "resources/"),
]

setup(
    name="AppTech",
    version="1.0",
    description="Descrizione del programma",
    executables=[Executable("main.py", base=None)],
)

Per creare un file di installazione come .msi o un'immagine .iso da un progetto Python
1. Generare il File Eseguibile

pip install cx_Freeze
Genera il file eseguibile con:

python setup.py build
Troverai il tuo .exe nella cartella build.

2. Convertire in MSI Una volta ottenuto il file .exe, usa cx_Freeze per generare un file .msi:

python setup.py bdist_msi
Troverai il file .msi nella cartella dist. Questo file può essere eseguito su altri computer per installare il tuo programma.
'''
import os
import PyInstaller.__main__

import os
import PyInstaller.__main__

def collect_files(folder, destination_folder):
    """
    Raccoglie tutti i file in una cartella e restituisce una lista di stringhe
    nel formato richiesto da PyInstaller (source:destination_folder).
    """
    files = []
    for file_name in os.listdir(folder):
        full_path = os.path.join(folder, file_name)
        if os.path.isfile(full_path):
            # Formatta per PyInstaller: "source:destination"
            files.append(f"{full_path}:{destination_folder}")
    return files

# Specifica le directory per risorse e database
resources_folder = "C:/PROGETTO/myapp/resources"
database_folder = "C:/PROGETTO/myapp/Database_Utilities/Database"

# Colleziona i file da includere
resources = collect_files(resources_folder, "resources")  # Include i file di risorse nella directory "resources"
database_files = collect_files(database_folder, "Database_Utilities/Database")  # Include i file di database nella destinazione appropriata

# Aggiungi manualmente i percorsi dei file necessari
manual_files = [
    "C:/PROGETTO/myapp/resources/geometric.jpg",
    "C:/PROGETTO/myapp/resources/Geometry_Texture.jpg",
    "C:/PROGETTO/myapp/resources/LogoCINCOTTI.jpg",
    "C:/PROGETTO/myapp/resources/LOGOjpeg.jpg",
    "C:/PROGETTO/myapp/resources/LOGOMOZZABELLAECINCOTTI SRLS.jpg",
    "C:/PROGETTO/myapp/resources/LOGOMOZZABELLAECINCOTTI.jpg",
    "C:/PROGETTO/myapp/resources/GhostTrain.json",
    "C:/PROGETTO/myapp/resources/A_professional_sleek_abstract_background_16_9.png",
    "C:/PROGETTO/myapp/resources/apps.png",
    "C:/PROGETTO/myapp/resources/apps_white.png",
    "C:/PROGETTO/myapp/resources/boxes.png",
    "C:/PROGETTO/myapp/resources/boxes_white.png",
    "C:/PROGETTO/myapp/resources/briefcase.png",
    "C:/PROGETTO/myapp/resources/briefcase_white.png",
    "C:/PROGETTO/myapp/resources/document.png",
    "C:/PROGETTO/myapp/resources/edit.png",
    "C:/PROGETTO/myapp/resources/home.png",
    "C:/PROGETTO/myapp/resources/home_white.png",
    "C:/PROGETTO/myapp/resources/insert-credit-card.png",
    "C:/PROGETTO/myapp/resources/insert-credit-card_white.png",
    "C:/PROGETTO/myapp/resources/lightbulb-on.png",
    "C:/PROGETTO/myapp/resources/lightbulb-on_white.png",
    "C:/PROGETTO/myapp/resources/money-check-edit.png",
    "C:/PROGETTO/myapp/resources/money-check-edit_white.png",
    "C:/PROGETTO/myapp/resources/shopping-cart.png",
    "C:/PROGETTO/myapp/resources/shopping-cart_white.png",
    "C:/PROGETTO/myapp/resources/truck-side.png",
    "C:/PROGETTO/myapp/resources/truck-side_white.png",
    "C:/PROGETTO/myapp/resources/users-alt.png",
    "C:/PROGETTO/myapp/resources/users-alt_white.png"

]

# Combina tutte le risorse
all_files = resources + database_files + manual_files

# Comando PyInstaller
PyInstaller.__main__.run([
    '--name=MyApp',  # Nome dell'app
    '--onefile',  # Genera un unico file eseguibile
    '--windowed',  # Evita di aprire il terminale (per applicazioni GUI)
    *(f'--add-data={file}' for file in all_files),  # Include tutte le risorse
    'main.py',  # File principale del tuo progetto
])
