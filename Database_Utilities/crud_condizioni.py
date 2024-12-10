from Database_Utilities.connection import _connection

def get_all_table1():
    """Restituisce tutti i record di 'table1'."""
    conn = _connection()
    cursor = conn.cursor()

    query = "SELECT id, nome FROM condizioni_pagamento"
    cursor.execute(query)
    records = [{"id": row[0], "nome": row[1]} for row in cursor.fetchall()]

    conn.close()
    return records


def get_table1_by_id(record_id):
    """Restituisce un record specifico di 'table1' basandosi sull'ID."""
    conn = _connection()
    cursor = conn.cursor()

    query = "SELECT id, nome FROM condizioni_pagamento WHERE id = %s"
    cursor.execute(query, (record_id,))
    record = cursor.fetchone()

    conn.close()
    return {"id": record[0], "nome": record[1]} if record else None


def add_table1_record(record_id, nome):
    """Aggiunge un nuovo record a 'table1'."""
    conn = _connection()
    cursor = conn.cursor()

    query = "INSERT INTO condizioni_pagamento (id, nome) VALUES (%s, %s)"
    cursor.execute(query, (record_id, nome))

    conn.commit()
    conn.close()


def update_table1_record(record_id, nome):
    """Aggiorna un record esistente in 'table1'."""
    conn = _connection()
    cursor = conn.cursor()

    query = "UPDATE condizioni_pagamento SET nome = %s WHERE id = %s"
    cursor.execute(query, (nome, record_id))

    conn.commit()
    conn.close()


def delete_table1_record(record_id):
    """Elimina un record specifico da 'table1'."""
    conn = _connection()
    cursor = conn.cursor()

    query = "DELETE FROM condizioni_pagamento WHERE id = %s"
    cursor.execute(query, (record_id,))

    conn.commit()
    conn.close()