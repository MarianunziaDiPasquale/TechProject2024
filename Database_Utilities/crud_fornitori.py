import sqlite3

db_path = 'Database_Utilities/Database/MergedDatabase.db'


def get_all_fornitori():
    '''Restituisce tutti i fornitori presenti nel database.'''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = 'SELECT DISTINCT Nome FROM fornitori'
    cursor.execute(query)
    fornitori = [row[0] for row in cursor.fetchall()]

    conn.close()
    return fornitori

def get_all_prodotti():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Eseguire la query per ottenere i nomi dei prodotti dalla colonna 'Descrizione'
    cursor.execute("SELECT Descrizione FROM prodotti;")
    product_names = cursor.fetchall()

    # Chiudere la connessione
    conn.close()

    # Restituire solo i nomi dei prodotti come una lista
    return [name[0] for name in product_names]




def get_prodotti_by_fornitore_name(fornitore_name):
    '''Restituisce i prodotti associati a un determinato fornitore.'''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = '''
        SELECT prodotti.Codice, prodotti.Descrizione, prodotti.ID_FORNITORE, 
               prodotti.COMPOSIZIONE_CARTONE, prodotti.PREZZO_VENDITA, prodotti.PREZZO_ACQUISTO
        FROM prodotti
        JOIN fornitori ON prodotti.ID_FORNITORE = fornitori.id
        WHERE fornitori.Nome = ?
    '''

    cursor.execute(query, (fornitore_name,))
    prodotti = [{'Codice': row[0], 'Descrizione': row[1], 'ID_FORNITORE': row[2],
                 'COMPOSIZIONE CARTONE': row[3], 'PREZZO VENDITA': row[4], 'PREZZO ACQUISTO': row[5]}
                for row in cursor.fetchall()]

    conn.close()
    return prodotti


def modify_prodotto(codice, descrizione, composizione_cartone, prezzo_vendita, prezzo_acquisto):
    '''Modifica i dati di un prodotto specifico nel database.'''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = '''
        UPDATE prodotti
        SET Descrizione = ?, COMPOSIZIONE_CARTONE = ?, PREZZO_VENDITA = ?, PREZZO_ACQUISTO = ?
        WHERE Codice = ?
    '''
    cursor.execute(query, (descrizione, composizione_cartone, prezzo_vendita, prezzo_acquisto, codice))

    conn.commit()
    conn.close()


def delete_prodotto(codice):
    '''Elimina un prodotto specifico dal database.'''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = 'DELETE FROM prodotti WHERE Codice = ?'
    cursor.execute(query, (codice,))

    conn.commit()
    conn.close()