from cx_Freeze import setup, Executable

setup(
    name="AppTech",
    version="1.0",
    description="Descrizione del programma",
    executables=[Executable("main.py", base=None)],
)

'''
Genera il file eseguibile con:

bash
Copia codice
python setup.py build
Troverai il tuo .exe nella cartella build.

2. Convertire in MSI Una volta ottenuto il file .exe, usa cx_Freeze per generare un file .msi:

bash
Copia codice
python setup.py bdist_msi
Troverai il file .msi nella cartella dist. Questo file può essere eseguito su altri computer per installare il tuo programma.
'''
