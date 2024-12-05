
from Database_Utilities.connection import _connection





def get_all_fornitori():
    '''Restituisce tutti i fornitori presenti nel database.'''
    conn = _connection()
    cursor = conn.cursor()

    query = 'SELECT DISTINCT Nome FROM fornitori'
    cursor.execute(query)
    fornitori = [row[0] for row in cursor.fetchall()]

    conn.close()
    return fornitori


# Modifica nella funzione `get_all_prodotti` in `crud_fornitori`
def get_all_prodotti():
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Codice, Descrizione FROM prodotti")
    prodotti = cursor.fetchall()
    conn.close()

    # Formatta ciascun prodotto come "Codice - Descrizione"
    return [f"{codice} - {descrizione}" for codice, descrizione in prodotti]


def get_prodotti_by_fornitore_name(fornitore_name):
    '''Restituisce i prodotti associati a un determinato fornitore.'''
    conn = _connection()
    cursor = conn.cursor()

    query = '''
        SELECT prodotti.Codice, prodotti.Descrizione, prodotti.ID_FORNITORE, 
               prodotti.COMPOSIZIONE_CARTONE, prodotti.PREZZO_VENDITA, prodotti.PREZZO_ACQUISTO
        FROM prodotti
        JOIN fornitori ON prodotti.ID_FORNITORE = fornitori.id
        WHERE fornitori.Nome = %s
    '''

    cursor.execute(query, (fornitore_name,))

    prodotti = [{'Codice': row[0], 'Descrizione': row[1], 'ID_FORNITORE': row[2],
                 'COMPOSIZIONE CARTONE': row[3], 'PREZZO VENDITA': row[4], 'PREZZO ACQUISTO': row[5]}
                for row in cursor.fetchall()]

    conn.close()
    return prodotti


def modify_prodotto(codice, descrizione, composizione_cartone, prezzo_vendita, prezzo_acquisto):
    '''Modifica i dati di un prodotto specifico nel database.'''
    conn = _connection()
    cursor = conn.cursor()

    query = '''
        UPDATE prodotti
        SET Descrizione = %s, COMPOSIZIONE_CARTONE = %s, PREZZO_VENDITA = %s, PREZZO_ACQUISTO = %s
        WHERE Codice = %s
    '''
    cursor.execute(query, (descrizione, composizione_cartone, prezzo_vendita, prezzo_acquisto, codice))

    conn.commit()
    conn.close()


def delete_prodotto(codice):
    '''Elimina un prodotto specifico dal database.'''
    conn = _connection()
    cursor = conn.cursor()

    query = 'DELETE FROM prodotti WHERE Codice = ?'
    cursor.execute(query, (codice,))

    conn.commit()
    conn.close()