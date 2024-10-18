import sqlite3

# Connessione al database (crea il database se non esiste)
conn = sqlite3.connect('Database_Utilities/Database/storico_database.db')
c = conn.cursor()

# Crea la tabella orders se non esiste
c.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id_ordine INTEGER PRIMARY KEY,
    data TEXT NOT NULL,
    cliente TEXT NOT NULL,
    prodotti TEXT NOT NULL,
    totale TEXT NOT NULL,
    fornitore TEXT NOT NULL
)
""")

# Inserisci dati di esempio nella tabella orders
c.execute("INSERT INTO orders (data, cliente, prodotti, totale, fornitore) VALUES ('2024-06-01', 'Mario Rossi', 'Prodotto A, Prodotto B', '100€', 'Fornitore A')")
c.execute("INSERT INTO orders (data, cliente, prodotti, totale, fornitore) VALUES ('2024-06-15', 'Luigi Bianchi', 'Prodotto C', '50€', 'Fornitore B')")
c.execute("INSERT INTO orders (data, cliente, prodotti, totale, fornitore) VALUES ('2024-07-01', 'Anna Verdi', 'Prodotto D', '200€', 'Fornitore C')")
c.execute("INSERT INTO orders (data, cliente, prodotti, totale, fornitore) VALUES ('2024-07-10', 'Giulia Neri', 'Prodotto E, Prodotto F', '150€', 'Fornitore A')")
c.execute("INSERT INTO orders (data, cliente, prodotti, totale, fornitore) VALUES ('2024-07-20', 'Carlo Bianchi', 'Prodotto G', '75€', 'Fornitore B')")
c.execute("INSERT INTO orders (data, cliente, prodotti, totale, fornitore) VALUES ('2024-08-01', 'Laura Rossi', 'Prodotto H', '120€', 'Fornitore C')")
c.execute("INSERT INTO orders (data, cliente, prodotti, totale, fornitore) VALUES ('2024-08-15', 'Marco Verdi', 'Prodotto I, Prodotto J', '180€', 'Fornitore A')")
c.execute("INSERT INTO orders (data, cliente, prodotti, totale, fornitore) VALUES ('2024-08-25', 'Sara Neri', 'Prodotto K', '90€', 'Fornitore B')")
c.execute("INSERT INTO orders (data, cliente, prodotti, totale, fornitore) VALUES ('2024-09-01', 'Paolo Bianchi', 'Prodotto L', '110€', 'Fornitore C')")
c.execute("INSERT INTO orders (data, cliente, prodotti, totale, fornitore) VALUES ('2024-09-10', 'Elena Rossi', 'Prodotto M', '130€', 'Fornitore A')")

# Commit delle modifiche e chiusura della connessione
conn.commit()
conn.close()

print("Database creato e popolato con successo.")