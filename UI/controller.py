import warnings

import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.squadra = ""

    def fillDDTeams(self):
        teams = self._model.getTeams()

        teamsDD = list(map(lambda x: ft.dropdown.Option(text=x, key=x), teams))
        self._view.ddTeams.options = teamsDD
        self._view.update_page()




    def handle_crea_grafo(self, e):
        self.squadra = self._view.ddTeams.value
        if self.squadra is None:
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text(f"Squadra non selezionata"))
            self._view.update_page()
            return

        self._model.buildGraph(self.squadra)
        n, e = self._model.graphDetails()
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato con {n} nodi e {e} archi"))
        self._view.update_page()

        self.fillDDYear()

    def fillDDYear(self):
        anni = DAO.getNodes(self.squadra)
        anniDD = list(map(lambda x: ft.dropdown.Option(x), anni))
        self._view.ddAnno.options = anniDD
        self._view.update_page()
    def handle_dettagli(self, e):
        self.anno = int(self._view.ddAnno.value)
        if self.anno is None:
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text(f"Anno non selezionata"))
            self._view.update_page()
            return

        dizio = self._model.getDettagli(self.anno)
        for i in dizio:
            self._view.txt_result.controls.append(ft.Text(f"{self.anno} <--> anno {i}, peso: {dizio[i]}"))
        self._view.update_page()


    def handleSimulazione(self, e):
        tifosi = self._view.txtTifosi.value
        if tifosi is None or tifosi=="":
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text(f"Numero tifosi non inserito"))
            self._view.update_page()
            return
        try:
            tifosiInt = int(tifosi)

        except ValueError:
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text(f"Numero tifosi non intero"))
            self._view.update_page()
            return

        risultato, tifosiPersi = self._model.simulazione(tifosiInt, self.anno, self.squadra)
        self._view.txt_result.controls.append(ft.Text(f"Numero tifosi persi: {tifosiPersi}"))
        for i in risultato:
            self._view.txt_result.controls.append(ft.Text(f"Il giocatore: {i} alla fine delle simulazione ha {risultato[i]} tifosi"))


        self._view.update_page()






