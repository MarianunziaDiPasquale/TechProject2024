from Database_Utilities.connection import _connection

def create_record_storico_ordini(codice_prodotto, id_cliente, numero_cartoni_venduti, data, ricavo_lordo):
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO storico_ordini (codice_prodotto, id_cliente, numero_cartoni_venduti, data, ricavo_lordo) VALUES (%s, %s, %s, %s, %s)",
        (codice_prodotto, id_cliente, numero_cartoni_venduti, data, ricavo_lordo))

    conn.commit()
    conn.close()
    print("Record inserted into storico_ordini.")

def read_records_storico_ordini():
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM storico_ordini")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_record_storico_ordini(codice_prodotto, id_cliente, new_numero_cartoni_venduti, new_data, new_ricavo_lordo):
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE storico_ordini SET numero_cartoni_venduti = %s, data = %s, ricavo_lordo = %s WHERE codice_prodotto = %s AND id_cliente = %s",
        (new_numero_cartoni_venduti, new_data, new_ricavo_lordo, codice_prodotto, id_cliente))

    conn.commit()
    conn.close()
    print("Record updated in storico_ordini.")

def delete_record_storico_ordini(codice_prodotto, id_cliente):
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM storico_ordini WHERE codice_prodotto = %s AND id_cliente = %s",
                   (codice_prodotto, id_cliente))
    conn.commit()
    conn.close()
    print("Record deleted from storico_ordini.")
