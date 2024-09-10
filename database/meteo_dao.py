# Importare le classi e i metodi necessari
from database.DB_connect import DBConnect
from model.situazione import Situazione

# Creare la classe MeteoDao
class MeteoDao():

    # Definire il metodo get_all_situazioni, che restituisce gli oggetti Situazioni a partire dai dati presenti nel
    # database
    @staticmethod
    def get_all_situazioni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                        FROM situazione s 
                        ORDER BY s.Data ASC"""
            cursor.execute(query)
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result

    # Definire il metodo get_media_umidita, che restituisce l'umidità media per ogni città nel mese selezionato
    # dall'utente tramite l'apposito menù a tendina
    def get_media_umidita(self, mese):
        # Creare la connessione
        cnx = DBConnect.get_connection()
        # Definire la query
        query = """SELECT AVG(s.Umidita), s.Localita
        FROM situazione s
        WHERE MONTH(s.Data) = %s
        GROUP BY S.Localita"""
        # Se la connessione al database non è avvenuta, verrà stampato un relativo messaggio di errore
        if cnx is None:
            print("Connessione fallita")
        # Altrimenti
        else:
            # Creare il cursore
            cursor = cnx.cursor()
            # Eseguire la query
            cursor.execute(query, (mese,))
            # Leggere tutte le righe
            rows = cursor.fetchall()
            # Chiudere il cursore
            cursor.close()
            # Chiudere la connessione
            cnx.close()
            # Restituire il risultato
            return rows

    # Definire il metodo get_primi_15_giorni, che identifica tutte le informazioni presenti nella tabella iniziale
    # situazione in riferimento ai primi quindici giorni del mese
    def get_primi_15_giorni(self, mese):
        # Creare la connessione
        cnx = DBConnect.get_connection()
        # Definire la query
        query = """SELECT s.Localita, s.Data, s.Umidita
        FROM situazione s
        WHERE MONTH(s.Data) = %s AND DAY(s.Data) < 16
        ORDER BY s.Data"""
        # Se la connessione al database non è avvenuta, verrà stampato un relativo messaggio di errore
        if cnx is None:
            print("Connessione fallita")
        # Altrimenti
        else:
            # Definire la lista vuota result
            result = []
            # Creare il cursore
            cursor = cnx.cursor()
            # Eseguire la query
            cursor.execute(query, (mese,))
            # Leggere tutte le righe
            rows = cursor.fetchall()
            # Per ogni riga, restituire l'oggetto costituito da località, data e umidità che sarà appeso nella lista,
            # inizialmente vuota, result
            for row in rows:
                result.append(Situazione(row[1], row[2], row[3]))
            # Chiudere il cursore
            cursor.close()
            # Chiudere la connessione
            cnx.close()
            # Restituire il risultato
        return result
