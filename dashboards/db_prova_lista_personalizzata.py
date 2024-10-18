import sqlite3

# Percorso del database
db_path = 'dashboards/Database_Utilities/liste_personalizzata.db'

# Creazione della connessione al database
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Creazione della tabella per i prodotti
c.execute('''
CREATE TABLE IF NOT EXISTS prodotti_clienti (
    RAGIONE_SOCIALE TEXT,
    ID TEXT,
    PRODOTTO TEXT,
    QUANTITA INTEGER
)
''')

# Dati di esempio da inserire per la tabella "prodotti_clienti"
prodotti_clienti_data = [
    ('18 SALE & PEPE - ITALFOODING', '796CQ', 'Prodotto A', 10),
    ('18 SALE & PEPE - ITALFOODING', '796CQ', 'Prodotto B', 20),
    ('18 SALE & PEPE - ITALFOODING', '796CQ', 'Prodotto C', 30),
    ('19 SALE & PEPE - ITALFOODING', '424VX', 'Prodotto A', 10),
    ('19 SALE & PEPE - ITALFOODING', '424VX', 'Prodotto C', 30),
    ('AMALFI - MOIRA RST', '716AB', 'Prodotto A', 10),
    ('AMALFI - MOIRA RST', '716AB', 'Prodotto B', 20),
    ('AMALFI - MOIRA RST', '716AB', 'Prodotto C', 30),
    ('AMORE DI FRANCESCA - I GEMELLI', '592EV', 'Prodotto A', 10),
    ('AMORE DI FRANCESCA - I GEMELLI', '592EV', 'Prodotto B', 20),
    ('AMORE DI FRANCESCA - I GEMELLI', '592EV', 'Prodotto C', 30),
    ('AMORVINO', '227JP', 'Prodotto A', 10),
    ('AMORVINO', '227JP', 'Prodotto B', 20),
    ('AMORVINO', '227JP', 'Prodotto C', 30)
]

# Inserimento dei dati di esempio nella tabella "prodotti_clienti"
c.executemany('''
INSERT INTO prodotti_clienti (RAGIONE_SOCIALE, ID, PRODOTTO, QUANTITA)
VALUES (?, ?, ?, ?)
''', prodotti_clienti_data)

# Commit delle modifiche e chiusura della connessione
conn.commit()
conn.close()

print("Dati inseriti nella tabella prodotti_clienti con successo!")

def get_prodotti_by_cliente(cliente_name):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = "SELECT RAGIONE_SOCIALE,ID,PRODOTTO,QUANTITA FROM prodotti_clienti WHERE `RAGIONE_SOCIALE` LIKE ?"
    cur.execute(query, ('%' + cliente_name + '%',))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_prodotti_by_cliente_1(cliente_name):
    """ Get all products and quantities for a cliente from the 'prodotti_clienti' table """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = "SELECT * FROM prodotti_clienti WHERE `RAGIONE_SOCIALE` LIKE ?"
    cur.execute(query, ('%' + cliente_name + '%',))
    prodotti_info = cur.fetchall()
    conn.close()

    if prodotti_info:
        # Get column names to create dictionaries for each product
        column_names = [description[0] for description in cur.description]
        prodotti_list = [dict(zip(column_names, prodotto)) for prodotto in prodotti_info]
        return prodotti_list
    else:
        return []