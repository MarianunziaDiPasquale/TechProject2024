import mysql.connector
from mysql.connector import Error

# Configura i dettagli della connessione
config = {
    "user": "amministratore",  # Sostituisci con il tuo nome utente
    "password": "gestionale_01",  # Sostituisci con la tua password
    "host": "gestionalec.mysql.database.azure.com",  # Host del server
    "port": 3306,  # Porta MySQL predefinita
    "database": "maindatabase",  # Sostituisci con il nome del tuo database
    "ssl_ca": "DigiCertGlobalRootCA.crt.pem",  # Path al certificato SSL scaricato da Azure
    "ssl_disabled": False,  # Assicura che SSL sia abilitato
}

# Prova la connessione
try:
    print("Tentativo di connessione al database...")
    cnx = mysql.connector.connect(**config)

    if cnx.is_connected():
        print("Connessione al database avvenuta con successo!")
    else:
        print("Connessione non riuscita.")
except Error as e:
    print(f"Errore durante la connessione: {e}")
finally:
    if 'cnx' in locals() and cnx.is_connected():
        cnx.close()
        print("Connessione chiusa.")


def _connection():
    cnx = mysql.connector.connect(**config)
    return cnx