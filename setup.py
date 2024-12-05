from cx_Freeze import setup, Executable

# Specifica i file di risorse
include_files = [
    ("resources", "resources")  # Include la cartella "resources"
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
