from Database_Utilities.connection import _connection

def create_record_vettori(id, nome, indirizzo):
    """
    Inserts a new record into the vettori table.
    """
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO vettori (id, nome, indirizzo) 
        VALUES (%s, %s, %s)
    """, (id, nome, indirizzo))

    conn.commit()
    conn.close()
    print("Record inserted into vettori.")

def read_records_vettori():
    """
    Retrieves all records from the vettori table.
    """
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vettori")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_record_vettori(id, new_nome, new_indirizzo):
    """
    Updates an existing record in the vettori table by ID.
    """
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE vettori 
        SET nome = %s, indirizzo = %s
        WHERE id = %s
    """, (new_nome, new_indirizzo, id))

    conn.commit()
    conn.close()
    print("Record updated in vettori.")

def delete_record_vettori(id):
    """
    Deletes a record from the vettori table by ID.
    """
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vettori WHERE id = %s", (id,))

    conn.commit()
    conn.close()
    print("Record deleted from vettori.")

def get_all_vettori_names():
    """
    Retrieves the names of all vettori from the vettori table.
    """
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM vettori")
    vettori = cursor.fetchall()
    conn.close()
    return [vettore[0] for vettore in vettori]

def get_vettore_info_by_name(nome):
    """
    Retrieves all information of a vettore by name from the vettori table.
    """
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vettori WHERE nome = %s", (nome,))
    vettore_info = cursor.fetchone()
    if vettore_info:
        column_names = [desc[0] for desc in cursor.description]
        vettore_dict = dict(zip(column_names, vettore_info))
        conn.close()
        return vettore_dict
    else:
        conn.close()
        return None
