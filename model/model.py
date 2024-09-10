# Importare copy
import copy

# Importare la classe MeteoDao dal modulo meteo_dao del package database
from database.meteo_dao import MeteoDao

# Creare la classe Model
class Model:

    # Definire il metodo __init__
    def __init__(self):
        self._dao = MeteoDao()
        self._costo_minimo = -1
        self._sequenza_ottima = []

    # Definire il metodo get_media_umidita, che restituisce il metodo get_media_umidita definito nel modulo meteo_dao
    # del package database
    def get_media_umidita(self, mese):
        return self._dao.get_media_umidita(mese)

    # Definire il metodo calcolo_sequenza, che calcola la sequenza che i tecnici dovranno seguire
    def calcola_sequenza(self, mese):
        # Resettare le informazioni iniziali quando si utilizza la ricorsione
        self._costo_minimo = -1
        self._sequenza_ottima = []
        # Definire le situazioni a metà mese
        situazioni_meta_mese = self._dao.get_primi_15_giorni(mese)
        # Svolgere su tali situazioni e sul parziale, inizialmente pari ad una lista vuota, il metodo _ricorsione
        self._ricorsione([], situazioni_meta_mese)
        # Restituire la sequenza e il costo
        return self._sequenza_ottima, self._costo_minimo

    # Definire il metodo _ricorsione
    def _ricorsione(self, parziale, situazioni):
        # Caso terminale
        if len(parziale) == 15:
            # Calcolare il costo che verrà fatto alla fine
            costo = self._calcola_costo(parziale)
            if (self._costo_minimo == -1) or (costo < self._costo_minimo):
                self._costo_minimo = costo
                self._sequenza_ottima = copy.deepcopy(parziale)
            # print(parziale) # aggiunto per verificare nella run
        # Altrimenti, la singola situazione verrà aggiunta al parziale richiamando il metodo ricorsivo e facendo il
        # backtraking
        else:
            # Viene implementato day in quanto per ogni giorno abbiamo i dati relativi a tre città e conviene
            # fare il ciclo for sulle situazioni inserendo tali parametri
            # Bisogna anche fare il controllo sui vincoli: un tecnico non può stare più di sei giorni in una stessa
            # città e deve rimanere al tempo stesso almeno tre giorni consecutivi nella città in cui si è spostato
            day = len(parziale) + 1
            for situazione in situazioni[(day-1)*3:day*3]:
                # Se i vincoli sono soddisfatti, allora la situazione verrà appesa al parziale e...
                if self._vincoli_soddisfatti(parziale, situazione):
                    parziale.append(situazione)
                    self._ricorsione(parziale, situazione)
                    parziale.pop()

    # Definire il metodo _vincoli_soddisfatti
    def _vincoli_soddisfatti(self, parziale, situazione) -> bool:
        # Fare un check per vedere se il tecnico non è stato già tre giorni nella stessa città
        counter = 0
        for fermata in parziale:
            if fermata.localita == situazione.localita:
                counter = counter + 1
        if counter >= 6:
            return False
        # Verificare che il tecnico rimanga in una città almeno tre giorni di fila
        # Per fare ciò bisogna verificare che nei tre giorni precedenti il tecnico rimanga nella stessa città
        # Se la lunghezza è minore o uguale a due e maggiore di zero e il tecnico cambia la località, allora verrà
        # restituito il valore False... il tecnico dovrà, infatti, ancora rimanere nella stessa città per almeno un
        # giorno
        if len(parziale) <= 2 and len(parziale) > 0:
            prima_fermata = parziale[0].localita
            if situazione.localita != prima_fermata:
                return False
        # Se la lunghezza del parziale ha almeno tre elementi, allora bisogna controllare gli ultimi tre elementi e
        # verificare che il tecnico si sia fermato per almeno tre giorni di fila nella stessa località
        elif len(parziale) > 2:
            sequenza_finale = parziale[-3:] # questo significa prendere gli ultimi tre elementi della sequenza, ossia
            # gli ultimi tre giorni del parziale
            prima_fermata = sequenza_finale[0].localita # indica la località relativa al primo degli ultimi tre giorni
            # selezionati
            counter = 0 # questo conteggio serve per verificare quanto tempo si ferma in una località
            for fermata in sequenza_finale:
                if fermata.localita == prima_fermata:
                    counter = counter + 1
            # Se il counter è minore di tre e la località di situazione è diversa dall'ultima località presa in
            # considerazione, allora verrà restituito il valore False
            if (counter < 3) and situazione.localita != sequenza_finale[-1].localita:
                return False
        # Se sono stati soddisfatti tutti i vincoli, allora viene restituito true
        return True

    # Definire il metodo _calcolo_costo, che calcola il costo finale cercando di minimizzarlo
    def _calcola_costo(self, parziale):
        costo = 0
        for i in range(len(parziale)):
            costo = costo + parziale[i].umidita
            # Primi due giorni
            if i == 2:
                if parziale[i].localita != parziale[0].localita:
                    costo = costo + 100
            # Altri giorni
            elif i > 2:
                ultime_fermate = parziale[i-2:i+1] # le ultime tre fermate
                if ultime_fermate[2].localita != ultime_fermate[0].localita or ultime_fermate[2].localita != ultime_fermate[1].localita:
                    costo = costo + 100
        return costo