# Importare flet
import flet as ft

# Importare le classi utili
from UI.view import View
from model.model import Model

# Definire la classe Controller
class Controller:

    # Definire il metodo __init__
    def __init__(self, view: View, model: Model):
        # The view, with the graphical elements of the UI
        self._view = view
        # The model, which implements the logic of the program and holds the data
        self._model = model
        # Other attributes
        self._mese = 0

    # Definire il metodo handle_umidita_media, che visualizza l'umidità media per ogni città nel mese selezionato
    def handle_umidita_media(self, e):
        # Leggere il valore del mese selezionato
        self._mese = self._view.dd_mese.value
        # Se il mese è ancora pari a zero, allora vuol dire che non è stato selezionato... bisogna, quindi, creare
        # un messaggio di avviso che segnali tale mancanza
        if self._mese == 0:
            self._view.create_alert("Selezionare il mese!")
            return
        # Pulire la list view
        self._view.lst_result.controls.clear()
        # Aggiungere alla list view il seguente testo
        self._view.lst_result.controls.append(ft.Text(f"L'umidità media per ogni città nel mese selezionato è:"))
        # Determinare le statistiche volute tramite l'apposito metodo get_media_umidita presente nel file model del
        # package model
        statistiche = self._model.get_media_umidita(self._mese)
        # Per ogni statistica presente, stampare nella list view la località e la sua media dell'umidità
        for statistica in statistiche:
            self._view.lst_result.controls.append(ft.Text(f"{statistica[1]}: {statistica[0]}"))
        # Aggiornare la pagina
        self._view.update_page()

    # Definire il metodo handle_sequenza, che visualizza il percorso migliore che il tecnico dovrà fare per minimizzare
    # i costi
    def handle_sequenza(self, e):
        # Leggere il valore del mese selezionato
        self._mese = self._view.dd_mese.value
        # Se il mese è ancora pari a zero, allora vuol dire che non è stato selezionato... bisogna, quindi, creare
        # un messaggio di avviso che segnali tale mancanza
        if self._mese == 0:
            self._view.create_alert("Selezionare il mese!")
            return
        # Pulire la list view
        self._view.lst_result.controls.clear()
        # Determinare la tupla sequenza, costo attraverso il corrispettivo metodo
        sequenza, costo = self._model.calcola_sequenza(self._mese)
        # Stampare il costo nella list view
        self._view.lst_result.controls.append(ft.Text(f"Il costo della sequenza è: {costo}"))
        # Per ogni fermata, stamparla nella list view
        for fermata in sequenza:
            self._view.lst_result.controls.append(ft.Text(fermata))
        self._view.update_page()