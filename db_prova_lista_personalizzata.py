import sqlite3
from Database_Utilities.connection import _connection

#print("Dati inseriti nella tabella prodotti_clienti con successo!")

def get_prodotti_by_cliente(cliente_name):
    conn = _connection()
    cur = conn.cursor()
    query = "SELECT RAGIONE_SOCIALE,ID,PRODOTTO,QUANTITA FROM prodotti_clienti WHERE `RAGIONE_SOCIALE` LIKE ?"
    cur.execute(query, ('%' + cliente_name + '%',))
    rows = cur.fetchall()
    conn.close()
    return rows
