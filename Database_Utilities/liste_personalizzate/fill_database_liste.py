import os
import pandas as pd
import sqlite3


# Funzione per leggere e processare ogni file Excel
def process_excel_file(file_path):
    # Carica il file Excel, escludendo le prime 4 righe
    df = pd.read_excel(file_path, skiprows=4)

    # Mantiene solo le righe dove la prima colonna è non vuota
    df = df.dropna(subset=[df.columns[0]])

    # Restituisce solo la prima colonna
    return df[df.columns[0]]


# Funzione principale per creare la tabella per ogni file
def create_table_from_excel_file(file_path, db_path):
    # Estrae il nome del file senza estensione e spazi
    table_name = os.path.splitext(os.path.basename(file_path))[0].replace(" ", "_")

    # Connessione al database SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Crea una nuova tabella con un solo campo "col1", racchiudendo il nome della tabella tra virgolette
    cursor.execute(f'CREATE TABLE IF NOT EXISTS "{table_name}" (col1 TEXT)')

    # Processa il file Excel e ottiene i dati della prima colonna
    col_data = process_excel_file(file_path)

    # Inserisce i dati nella tabella
    for value in col_data:
        cursor.execute(f'INSERT INTO "{table_name}" (col1) VALUES (?)', (value,))

    # Commit e chiusura della connessione al database
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Ottiene la directory corrente (dove si trova il file Python)
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Specifica il percorso del database
    db_path = 'percorso_del_tuo_database.db'  # Sostituisci con il percorso del database

    # Legge tutti i file .xlsx nella directory corrente
    for filename in os.listdir(current_directory):
        if filename.endswith('.xlsx'):
            print(f"Elaborando il file: {filename}")

            # Percorso completo del file
            file_path = os.path.join(current_directory, filename)

            # Crea una tabella e inserisce i dati per ogni file
            create_table_from_excel_file(file_path, db_path)

    print("Tutte le tabelle sono state create con successo nel database.")
