import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = [2015, 2016, 2017, 2018]
        self._listColor = self._model.colors

    def fillDD(self):
        """
        Riempie i due menu a tendina
        """
        for i in self._listYear:
            self._view._ddyear.options.append(ft.dropdown.Option(f"{i}"))
        for color in self._listColor:
            self._view._ddcolor.options.append(ft.dropdown.Option(color))
        self._view.update_page()

    def handle_graph(self, e):
        if self._view._ddyear.value is None:
            self._view.create_alert("Selezionare un anno")
        elif self._view._ddcolor.value is None:
            self._view.create_alert("Selezionare un anno")
        else:
            year = int(self._view._ddyear.value)
            color = self._view._ddcolor.value
            self._model.build_graph(year, color)
            self.print_graph()
            self.fillDDProduct()  #riempo il menu a tendina con i nodi del grafo

    def print_graph(self):
        self._view.txtOut.controls.clear()
        self._view.txtOut.controls.append(ft.Text(f"Numero di vertici: {self._model.num_nodes()} "
                                                  f"Numero di archi: {self._model.num_edges()}"))
        for arco in self._model.max_weight:
            self._view.txtOut.controls.append(ft.Text(f"Arco da {arco[0]} a {arco[1]}, peso={arco[2]["weight"]}"))
        self._view.txtOut.controls.append(ft.Text(f"I nodi ripetuti sono: {self._model.duplicati}"))
        self._view.update_page()

    def fillDDProduct(self):
        self._view._ddnode.options.clear()
        for product in self._model.products_graph.nodes:
            self._view._ddnode.options.append(ft.dropdown.Option(
                data=product,
                text=product.Product_number,
                on_click=self.read_product
            ))
        self._view.update_page()

    def read_product(self, e):
        self._view._ddnode.data = e.control.data

    def handle_search(self, e):
        if self._view._ddnode.data is None:
            self._view.create_alert("Selezionare un prodotto")
        else:
            v0 = self._view._ddnode.data
            self._model.get_percorso(v0)
            self.print_search()

    def print_search(self):
        self._view.txtOut2.controls.clear()
        self._view.txtOut2.controls.append(ft.Text(f"Numero di archi percorso più lungo: {len(self._model.soluzione)}"))
        self._view.update_page()
