# Importare flet
import flet as ft

# Importare le varie classi utili
from model.model import Model
from UI.view import View
from UI.controller import Controller

# Definire il main, tramite il quale collaboreranno modello, interfaccia grafica e controller
def main(page: ft.Page):
    my_model = Model()
    my_view = View(page)
    my_controller = Controller(my_view, my_model)
    my_view.set_controller(my_controller)
    my_view.load_interface()

# Implementare il seguente codice per visualizzare l'interfaccia grafica
ft.app(target=main)