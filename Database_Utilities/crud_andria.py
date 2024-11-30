
from Database_Utilities.connection import _connection

def create_record_andria(codice_prodotto, esistenze, cartoni):
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO andria (Codice, Esistenze, Cartoni) VALUES (?, ?, ?)",
                   (codice_prodotto, esistenze, cartoni))
    conn.commit()
    conn.close()
    print("Record inserted into andria.")

def read_records_andria():
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM andria")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_record_andria(codice_prodotto, new_esistenze, new_cartoni):
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE andria SET Esistenze = ?, Cartoni = ? WHERE Codice = ?",
                   (new_esistenze, new_cartoni, codice_prodotto))
    conn.commit()
    conn.close()
    print("Record updated in andria.")

def delete_record_andria(codice_prodotto):
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM andria WHERE Codice = ?", (codice_prodotto,))
    conn.commit()
    conn.close()
    print("Record deleted from andria.")


def transfer_quantity_from_andria_to_parigi(codice_prodotto, quantity_to_transfer):
    conn = _connection()
    cursor = conn.cursor()

    # Check if the product exists in andria
    cursor.execute("SELECT * FROM andria WHERE Codice = ?", (codice_prodotto,))
    record_andria = cursor.fetchone()

    if not record_andria or record_andria[1] < quantity_to_transfer:
        print("Error: Insufficient quantity in andria for transfer.")
        return

    # Check if the product already exists in parigi
    cursor.execute("SELECT * FROM parigi WHERE Codice = ?", (codice_prodotto,))
    record_parigi = cursor.fetchone()

    if record_parigi:
        # Update the existing record in parigi (only the quantity 'Esistenze')
        cursor.execute(
            "UPDATE parigi SET Esistenze = Esistenze + ? WHERE Codice = ?",
            (quantity_to_transfer, codice_prodotto)
        )
    else:
        # Create a new record in parigi with the transferred quantity
        cursor.execute(
            "INSERT INTO parigi (Codice, Esistenze, Cartoni) VALUES (?, ?, 0)",
            (codice_prodotto, quantity_to_transfer)
        )

    # Subtract the transferred quantity from andria (only 'Esistenze')
    cursor.execute(
        "UPDATE andria SET Esistenze = Esistenze - ? WHERE Codice = ?",
        (quantity_to_transfer, codice_prodotto)
    )

    conn.commit()
    conn.close()
