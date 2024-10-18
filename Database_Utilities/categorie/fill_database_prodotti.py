import pandas as pd
import sqlite3

# Carica il file Excel (escludendo la prima riga)
file_path = 'name.xlsx'  # Sostituisci con il percorso corretto del file
df = pd.read_excel(file_path)

# Escludere la prima riga (se è un'intestazione) e le righe dove la prima colonna è vuota
df = df.iloc[1:]  # Esclude la prima riga (che può essere l'intestazione)
df = df.dropna(subset=[df.columns[0]])  # Mantiene solo le righe con la prima colonna non vuota

# Sostituire i valori mancanti (NaN) con 0
df = df.fillna(0)

# Connessione al database SQLite
conn = sqlite3.connect('../Database/MergedDatabase.db')  # Sostituisci con il percorso del tuo database
cursor = conn.cursor()

# Inserimento dei dati nella tabella specifica
for _, row in df.iterrows():
    # Estrai i valori dalle colonne (sostituisci con i tuoi campi specifici)
    col1 = row[0]
    col2 = row[1]
    col3 = row[2]
    col4 = row[3]
    col5 = row[4]
    col6 = row[5]

    # Query di inserimento (sostituisci con i nomi corretti delle colonne della tua tabella)
    cursor.execute('''
        INSERT INTO prodotti (Codice, Descrizione, ID_FORNITORE, COMPOSIZIONE_CARTONE, PREZZO_VENDITA, PREZZO_ACQUISTO)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (col1, col2, col3, col4, col5, col6))

# Commit e chiusura connessione
conn.commit()
conn.close()
