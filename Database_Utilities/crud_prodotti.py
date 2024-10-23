import sqlite3

# Path to the SQLite database
db_path = 'Database_Utilities/Database/Magazzino.db'

def create_record_prodotti(codice, descrizione, fornitore, composizione_cartone, prezzo_vendita, prezzo_acquisto):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO prodotti (Codice, Descrizione, FORNITORE, 'COMPOSIZIONE CARTONE', 'PREZZO VENDITA', 'PREZZO ACQUISTO') VALUES (?, ?, ?, ?, ?, ?)",
                   (codice, descrizione, fornitore, composizione_cartone, prezzo_vendita, prezzo_acquisto))
    conn.commit()
    conn.close()
    print("Record inserted into prodotti.")

def read_records_prodotti():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prodotti")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_record_prodotti(codice, new_descrizione, new_fornitore, new_composizione_cartone, new_prezzo_vendita, new_prezzo_acquisto):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE prodotti SET Descrizione = ?, FORNITORE = ?, 'COMPOSIZIONE CARTONE' = ?, 'PREZZO VENDITA' = ?, 'PREZZO ACQUISTO' = ? WHERE Codice = ?",
                   (new_descrizione, new_fornitore, new_composizione_cartone, new_prezzo_vendita, new_prezzo_acquisto, codice))
    conn.commit()
    conn.close()
    print("Record updated in prodotti.")

def delete_record_prodotti(codice):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM prodotti WHERE Codice = ?", (codice,))
    conn.commit()
    conn.close()
    print("Record deleted from prodotti.")





def search_record_by_code(codice):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prodotti WHERE Codice = ?", (codice,))
    rows = cursor.fetchall()
    conn.close()
    return rows