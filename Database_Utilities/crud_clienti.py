import sqlite3

# Path to the SQLite database
db_path = 'Database_Utilities/Database/Magazzino.db'

def create_record_clienti(ragione_sociale, seconda_riga, indirizzo, cap, citta, nazione, partita_iva, telefono, email, zona, giorni_chiusura, orari_scarico, condizioni_pagamento, sconto, agente, id_cliente):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO clienti (Ragione_sociale, '2° riga rag. sociale', Indirizzo, CAP, Città, Nazione, 'Partita iva estero', Telefono, Email, Zona, 'Giorni di chiusura ', 'Orari di scarico', 'Condizioni pagamamento', Sconto, 'Agente 1', ID) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                   (ragione_sociale, seconda_riga, indirizzo, cap, citta, nazione, partita_iva, telefono, email, zona, giorni_chiusura, orari_scarico, condizioni_pagamento, sconto, agente, id_cliente))
    conn.commit()
    conn.close()
    print("Record inserted into clienti.")

def read_records_clienti():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clienti")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_record_clienti(ragione_sociale, new_seconda_riga, new_indirizzo, new_cap, new_citta, new_nazione, new_partita_iva, new_telefono, new_email, new_zona, new_giorni_chiusura, new_orari_scarico, new_condizioni_pagamento, new_sconto, new_agente, id_cliente):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""UPDATE clienti SET '2° riga rag. sociale' = ?, Indirizzo = ?, CAP = ?, Città = ?, Nazione = ?, 'Partita iva estero' = ?, Telefono = ?, Email = ?, Zona = ?, 'Giorni di chiusura ' = ?, 'Orari di scarico' = ?, 'Condizioni pagamamento' = ?, Sconto = ?, 'Agente 1' = ? 
                      WHERE Ragione_sociale = ? AND ID = ?""",
                   (new_seconda_riga, new_indirizzo, new_cap, new_citta, new_nazione, new_partita_iva, new_telefono, new_email, new_zona, new_giorni_chiusura, new_orari_scarico, new_condizioni_pagamento, new_sconto, new_agente, ragione_sociale, id_cliente))
    conn.commit()
    conn.close()
    print("Record updated in clienti.")

def delete_record_clienti(id_cliente):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clienti WHERE ID = ?", (id_cliente,))
    conn.commit()
    conn.close()
    print("Record deleted from clienti.")



def get_all_clienti_names():
    """ Get the names of all clienti from the 'clienti' table """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = "SELECT `Ragione sociale` FROM clienti;"
    cur.execute(query)
    clienti = cur.fetchall()
    conn.close()
    return [cliente[0] for cliente in clienti]



def get_cliente_info_by_name(cliente_name):
    """ Get all information of a cliente by name from the 'clienti' table """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = "SELECT * FROM clienti WHERE `Ragione sociale` = ?"
    cur.execute(query, (cliente_name,))
    cliente_info = cur.fetchone()
    conn.close()

    if cliente_info:
        # Get column names to create a dictionary
        column_names = [description[0] for description in cur.description]
        cliente_dict = dict(zip(column_names, cliente_info))
        return cliente_dict
    else:
        return None
