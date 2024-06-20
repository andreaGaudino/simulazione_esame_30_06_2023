import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.ddyear = None
        self.ddshape = None
        self.btn_graph = None
        self.txt_result = None
        self.txt_container = None

        self.txtN = None
        self.txtOut2 = None
        self.btn_path = None


    def load_interface(self):
        # title
        self._title = ft.Text("simulazione esame 30/06/2023", color="blue", size=24)
        self._page.controls.append(self._title)

        #row 1
        self.ddTeams = ft.Dropdown(label="Scegli una squadra")
        self.btn_graph = ft.ElevatedButton(text="Crea grafo", on_click=self._controller.handle_crea_grafo)

        row1 = ft.Row([ft.Container(self.ddTeams, width=300),
                      ft.Container(self.btn_graph, width=300)], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)
        self._controller.fillDDTeams()


        #row2

        self.ddAnno = ft.Dropdown(label="Anno")
        self.btnDettagli = ft.ElevatedButton(text="Dettagli grafo", on_click=self._controller.handle_dettagli)
        row2 = ft.Row([ft.Container(self.ddAnno, width=300),
                      ft.Container(self.btnDettagli, width=300)], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)
        #self._controller.fillDDYear()

        #row3
        self.txtTifosi = ft.TextField(label="Tifosi")
        self.btnSimulaTifosi = ft.ElevatedButton(text="Simula tifosi", on_click=self._controller.handleSimulazione)
        row3 = ft.Row([ft.Container(self.txtTifosi, width=300),
                      ft.Container(self.btnSimulaTifosi, width=300)], alignment=ft.MainAxisAlignment.CENTER)



        self.txt_result = ft.ListView(expand=1, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.controls.append(row3)
        self._page.update()
    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
