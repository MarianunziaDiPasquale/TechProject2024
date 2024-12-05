from Database_Utilities.connection import _connection

def create_record_prodotti(codice, descrizione, fornitore, composizione_cartone, prezzo_vendita, prezzo_acquisto):
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO prodotti (Codice, Descrizione, FORNITORE, `COMPOSIZIONE CARTONE`, `PREZZO VENDITA`, `PREZZO ACQUISTO`) VALUES (%s, %s, %s, %s, %s, %s)",
        (codice, descrizione, fornitore, composizione_cartone, prezzo_vendita, prezzo_acquisto))
    conn.commit()
    conn.close()
    print("Record inserted into prodotti.")

def read_records_prodotti():
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prodotti")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_record_prodotti(codice, new_descrizione, new_fornitore, new_composizione_cartone, new_prezzo_vendita, new_prezzo_acquisto):
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE prodotti SET Descrizione = %s, FORNITORE = %s, `COMPOSIZIONE CARTONE` = %s, `PREZZO VENDITA` = %s, `PREZZO ACQUISTO` = %s WHERE Codice = %s",
        (new_descrizione, new_fornitore, new_composizione_cartone, new_prezzo_vendita, new_prezzo_acquisto, codice))
    conn.commit()
    conn.close()
    print("Record updated in prodotti.")

def delete_record_prodotti(codice):
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM prodotti WHERE Codice = %s", (codice,))

    conn.commit()
    conn.close()
    print("Record deleted from prodotti.")





def search_record_by_code(codice):
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prodotti WHERE Codice = %s", (codice,))

    rows = cursor.fetchall()
    conn.close()
    return rows