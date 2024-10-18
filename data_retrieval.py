import sqlite3
from Database_Utilities.crud_clienti import get_all_clienti_names
from Database_Utilities.crud_fornitori import get_all_fornitori

db_path = 'Database_Utilities/Database/Magazzino.db'
print(db_path)

def create_connection(db_path):
    """ Create a database connection to the SQLite database """
    conn = sqlite3.connect(db_path)
    return conn

def get_existing_names(item_type):
    conn = create_connection(db_path)
    c = conn.cursor()
    if item_type == "Cliente":
        names = get_all_clienti_names()  # Already returns a list of names
    elif item_type == "Fornitore":
        names = get_all_fornitori()  # Already returns a list of names
    elif item_type == "Prodotto":
        c.execute("SELECT DISTINCT Nome FROM prodotti")
        names = [row[0] for row in c.fetchall()]
    conn.close()
    return names

def delete_records_by_name(item_type, name):
    conn = create_connection(db_path)
    c = conn.cursor()
    if item_type == "Cliente":
        c.execute("DELETE FROM clienti WHERE Ragione_sociale = ?", (name,))
    elif item_type == "Fornitore":
        c.execute("DELETE FROM fornitori WHERE Nome = ?", (name,))
        c.execute("DELETE FROM prodotti WHERE fornitore = ?", (name,))
    elif item_type == "Prodotto":
        c.execute("DELETE FROM prodotti WHERE Nome = ?", (name,))
    conn.commit()
    conn.close()

def create_record_clienti(ragione_sociale, seconda_riga, indirizzo, cap, citta, nazione, partita_iva, telefono, email, zona, giorni_chiusura, orari_scarico, condizioni_pagamento, sconto, agente, id_cliente):
    conn = create_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO clienti (Ragione_sociale, '2° riga rag. sociale', Indirizzo, CAP, Città, Nazione, 'Partita iva estero', Telefono, Email, Zona, 'Giorni di chiusura ', 'Orari di scarico', 'Condizioni pagamamento', Sconto, 'Agente 1', ID) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                   (ragione_sociale, seconda_riga, indirizzo, cap, citta, nazione, partita_iva, telefono, email, zona, giorni_chiusura, orari_scarico, condizioni_pagamento, sconto, agente, id_cliente))
    conn.commit()
    conn.close()
    print("Record inserted into clienti.")

def create_fornitore(name, id_fornitore):
    conn = create_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO fornitori (Nome, ID) VALUES (?, ?)", (name, id_fornitore))
    conn.commit()
    conn.close()
    print("Record inserted into fornitori.")

def create_record_prodotti(codice, descrizione, fornitore, composizione_cartone, prezzo_vendita, prezzo_acquisto):
    conn = create_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO prodotti (Codice, Descrizione, FORNITORE, 'COMPOSIZIONE CARTONE', 'PREZZO VENDITA', 'PREZZO ACQUISTO') VALUES (?, ?, ?, ?, ?, ?)",
                   (codice, descrizione, fornitore, composizione_cartone, prezzo_vendita, prezzo_acquisto))
    conn.commit()
    conn.close()
    print("Record inserted into prodotti.")
