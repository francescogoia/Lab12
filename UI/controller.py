import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        countries = self._model._list_countries
        years = ["2015", "2016", "2017", "2018"]
        for c in countries:
            self._view.ddcountry.options.append(ft.dropdown.Option(c))
        for y in years:
            self._view.ddyear.options.append(ft.dropdown.Option(y))

        self._view.update_page()



    def handle_graph(self, e):
        country = self._view.ddcountry.value
        anno = self._view.ddyear.value
        self._model.build_graph(country, anno)
        self._view.txt_result.controls.append(ft.Text(self._model.info_grafo()))

        self._view.update_page()

    def handle_volume(self, e):
        self._model.calcola_volumi()
        retailer_ordinati = self._model.ordina_retailer_per_volume()
        for r in retailer_ordinati:
            self._view.txtOut2.controls.append(ft.Text(r))

        self._view.update_page()

    def handle_path(self, e):
        num_archi = self._view.txtN.value
        int_num_archi = 0
        try:
            int_num_archi = int(num_archi)
        except ValueError:
            self._view.txtOut3.controls.append(ft.Text(f"Inserire un numero intero maggiore di 2"))

        best_peso, best_percorso = self._model.calcola_percorso(int_num_archi)
        self._view.txtOut3.controls.append(ft.Text(f"Peso cammino massimo: {best_peso}"))
        for i in best_percorso:
            self._view.txtOut3.controls.append(ft.Text(f"{i[0]} --> {i[1]}: {i[2]}"))

        self._view.update_page()