
import sqlite3

# Path to the SQLite database
db_path = 'dashboards/Database_Utilities/Fresh_MergedDatabase_with_Copied_Records.db'

def create_record_parigi(codice_prodotto, esistenze, cartoni):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO parigi (Codice, Esistenze, Cartoni) VALUES (?, ?, ?)",
                   (codice_prodotto, esistenze, cartoni))
    conn.commit()
    conn.close()
    print("Record inserted into parigi.")

def read_records_parigi():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM parigi")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_record_parigi(codice_prodotto, new_esistenze, new_cartoni):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE parigi SET Esistenze = ?, Cartoni = ? WHERE Codice = ?",
                   (new_esistenze, new_cartoni, codice_prodotto))
    conn.commit()
    conn.close()
    print("Record updated in parigi.")

def delete_record_parigi(codice_prodotto):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM parigi WHERE Codice = ?", (codice_prodotto,))
    conn.commit()
    conn.close()
    print("Record deleted from parigi.")
