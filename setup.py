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

'''

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
