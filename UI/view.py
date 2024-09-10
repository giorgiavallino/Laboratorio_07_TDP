# Importare flet
import flet as ft

# Definire la classe View
class View(ft.UserControl):

    # Definire il metodo __init__
    def __init__(self, page: ft.Page):
        super().__init__()
        # Page stuff
        self._page = page
        self._page.title = "Laboratorio 07 - Ricorsione"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # Controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # Graphical elements
        self._title = None
        self.dd_mese: ft.Dropdown = None
        self.btn_umidita: ft.ElevatedButton = None
        self.btn_calcola_sequenza: ft.ElevatedButton = None
        self.lst_result: ft.ListView = None

    # Definire il metodo load_interfaccia, che genera l'interfaccia grafica che sarà visualizzata dall'utente
    def load_interface(self):
        # Title
        self._title = ft.Text("Analisi meteo", color="blue", size=24)
        self._page.controls.append(self._title)

        # Row with some controls
        self.dd_mese = ft.Dropdown(options=[ft.dropdown.Option(key="01", text="gennaio"),
                                            ft.dropdown.Option(key="02", text="febbraio"),
                                            ft.dropdown.Option(key="03", text="marzo"),
                                            ft.dropdown.Option(key="04", text="aprile"),
                                            ft.dropdown.Option(key="05", text="maggio"),
                                            ft.dropdown.Option(key="06", text="giugno"),
                                            ft.dropdown.Option(key="07", text="luglio"),
                                            ft.dropdown.Option(key="08", text="agosto"),
                                            ft.dropdown.Option(key="09", text="settembre"),
                                            ft.dropdown.Option(key="10", text="ottobre"),
                                            ft.dropdown.Option(key="11", text="novembre"),
                                            ft.dropdown.Option(key="12", text="dicembre"),],
                                   label="mese",
                                   width=200,
                                   hint_text="Selezionare un mese")

        self.btn_umidita = ft.ElevatedButton(text="Umidità media",
                                             tooltip="Verifica l'umidità media per città, nel mese selezionato",
                                             on_click=self._controller.handle_umidita_media)

        self.btn_calcola_sequenza = ft.ElevatedButton(text="Calcola sequenza",
                                             tooltip="Calcola la sequenza ottimale per le analisi",
                                             on_click=self._controller.handle_sequenza)
        row1 = ft.Row([self.dd_mese, self.btn_umidita, self.btn_calcola_sequenza],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        # List view where the reply is printed
        self.lst_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.lst_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    # Definire il metodo create_alert, che crea un messaggio di avviso nell'interfaccia grafica
    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    # Definire il metodo update_page, che fa l'update della pagina
    def update_page(self):
        self._page.update()
