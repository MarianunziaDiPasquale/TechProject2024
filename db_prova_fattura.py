import sqlite3

# Percorso del database
db_path = 'resources/orders_fattura_1.db'

# Creazione della connessione al database
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Creazione della tabella orders_fattura se non esiste già
c.execute('''
CREATE TABLE IF NOT EXISTS orders_fattura (
    invoice_number TEXT,
    number TEXT,
    Date_1 TEXT,
    customer_phone TEXT,
    customer_address TEXT,
    id TEXT,
    customer_email TEXT,
    vat_number TEXT,
    nation TEXT,
    iban TEXT,
    swift TEXT,
    agent_name TEXT,
    payment_condition TEXT,
    sender_name TEXT,
    sender_giorno TEXT,
    article TEXT,
    product_description TEXT,
    product_quantity INTEGER,
    product_price REAL,
    product_discount REAL,
    product_amount REAL,
    total_quantity INTEGER,
    total_amount REAL,
    iva_amount REAL,
    courier_service TEXT,
    recipient TEXT,
    total_invoice_euro REAL
)
''')

# Dati di esempio da inserire
orders_fattura_data = [
    (
        'INV001', '1', '2024-08-30', '1234567890', 'Via Roma 1, Roma', '1',
        'mario.rossi@example.com', 'IT12345678901', 'Italia', 'IT60X0542811101000000123456', 'BICPLITMMXXX',
        'Luigi Verdi', '30 days', 'Sender SRL', '10:00:00',
        'ART001', 'Product 1 Description', 10, 100.50, 5, 95.50, 10, 955, 210, 'DHL', 'Recipient Name', 1355
    ),
    (
        'INV002', '2', '2024-08-31', '0987654321', 'Via Milano 5, Milano', '2',
        'giulia.bianchi@example.com', 'IT65432109876', 'Italia', 'IT60X0542811101000000654321', 'BICPLITMMXXX',
        'Anna Rossi', '15 days', 'Sender SPA', '',
        'ART002', 'Product 2 Description', 5, 50.00, 0, 50.00, 5, 250, 55, 'DHL', 'Recipient Name', 360
    ),
    (
        'INV003', '3', '2024-09-01', '5432109876', 'Via Napoli 10, Napoli', '3',
        'antonio.rossi@example.com', 'IT87654321098', 'Italia', 'IT60X0542811101000000987654', 'BICPLITMMXXX',
        'Marco Verdi', '7 days', 'Sender SNC', '09:00:00',
        'ART003', 'Product 3 Description', 20, 200.00, 10, 180.00, 20, 3600, 792, 'DHL', 'Recipient Name', 5184
    ),
(
        'INV004', '4', '2024-09-02', '9876543210', 'Via Firenze 15, Firenze', '4',
        'laura.verdi@example.com', 'IT10987654321', 'Italia', 'IT60X0542811101000000109876', 'BICPLITMMXXX',
        'Roberto Bianchi', '45 days', 'Sender SpA', '11:00:00',
        'ART004', 'Product 4 Description', 15, 150.00, 0, 150.00, 15, 2250, 495, 'UPS', 'Recipient Name', 2745
    ),
    (
        'INV005', '5', '2024-09-03', '5678901234', 'Via Torino 20, Torino', '5',
        'paolo.rossi@example.com', 'IT56789012345', 'Italia', 'IT60X0542811101000000567890', 'BICPLITMMXXX',
        'Giuseppe Rossi', '60 days', 'Sender SRL', '10:30:00',
        'ART005', 'Product 5 Description', 8, 80.00, 5, 76.00, 8, 608, 134, 'DHL', 'Recipient Name', 742
    ),
    (
        'INV006', '6', '2024-09-04', '1234567890', 'Via Venezia 25, Venezia', '6',
        'anna.bianchi@example.com', 'IT12345678901', 'Italia', 'IT60X0542811101000000612345', 'BICPLITMMXXX',
        'Maria Bianchi', '30 days', 'Sender SNC', '12:00:00',
        'ART006', 'Product 6 Description', 12, 120.00, 8, 110.40, 12, 1324.8, 291.46, 'UPS', 'Recipient Name', 1616.26
    )

]

# Inserimento dei dati di esempio
c.executemany('''
INSERT INTO orders_fattura (
    invoice_number, number, Date_1, customer_phone, customer_address, id,
    customer_email, vat_number, nation, iban, swift, agent_name,
    payment_condition, sender_name, sender_giorno,
    article, product_description, product_quantity,
    product_price, product_discount, product_amount,
    total_quantity, total_amount, iva_amount,
    courier_service, recipient, total_invoice_euro
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', orders_fattura_data)

# Commit delle modifiche e chiusura della connessione
conn.commit()
conn.close()

print("Dati di esempio inseriti nel database orders_fattura.db con successo!")
