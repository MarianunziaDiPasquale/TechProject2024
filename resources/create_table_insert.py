import sqlite3

# Creazione del database
conn = sqlite3.connect('city_data.db')
c = conn.cursor()
# Creazione della tabella
c.execute('''
CREATE TABLE IF NOT EXISTS city_data (
    id INTEGER PRIMARY KEY,
    city TEXT NOT NULL,
    codice TEXT NOT NULL,
    nome_prodotto TEXT NOT NULL,
    esistenti INTEGER NOT NULL,
    cartoni INTEGER NOT NULL
)
''')

# Inserimento dei dati (solo se la tabella è vuota)
c.execute("INSERT INTO city_data (city, codice, nome_prodotto, esistenti, cartoni) VALUES ('Andria', 'A001', 'Prodotto1', 100, 10)")
c.execute("INSERT INTO city_data (city, codice, nome_prodotto, esistenti, cartoni) VALUES ('Andria', 'A002', 'Prodotto2', 150, 15)")
c.execute("INSERT INTO city_data (city, codice, nome_prodotto, esistenti, cartoni) VALUES ('Parigi', 'P001', 'Prodotto3', 200, 20)")
c.execute("INSERT INTO city_data (city, codice, nome_prodotto, esistenti, cartoni) VALUES ('Parigi', 'P002', 'Prodotto4', 250, 25)")

conn.commit()
conn.close()