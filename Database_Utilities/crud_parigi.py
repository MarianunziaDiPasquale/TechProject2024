

from Database_Utilities.connection import _connection


def create_record_parigi(codice_prodotto, esistenze, cartoni):
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO parigi (Codice, Esistenze, Cartoni) VALUES (?, ?, ?)",
                   (codice_prodotto, esistenze, cartoni))
    conn.commit()
    conn.close()
    print("Record inserted into parigi.")

def read_records_parigi():
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM parigi")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_record_parigi(codice_prodotto, new_esistenze, new_cartoni):
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE parigi SET Esistenze = ?, Cartoni = ? WHERE Codice = ?",
                   (new_esistenze, new_cartoni, codice_prodotto))
    conn.commit()
    conn.close()
    print("Record updated in parigi.")

def delete_record_parigi(codice_prodotto):
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM parigi WHERE Codice = ?", (codice_prodotto,))
    conn.commit()
    conn.close()
    print("Record deleted from parigi.")
