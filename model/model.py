import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.colors = DAO.get_all_colors()
        self.products_by_color = []
        self.products_graph = nx.Graph()
        self.max_weight = []
        self.duplicati = set()
        self.soluzione = []

    def build_graph(self, year, color):
        self.max_weight = []  #resetto la lista dei max
        self.duplicati = set()  #resetto l'insieme dei duplicati
        self.products_graph.clear()  #resetto il grafo
        self.products_by_color = DAO.get_products_by_color(color)
        self.products_graph.add_nodes_from(self.products_by_color)
        for p in self.products_graph.nodes:
            for pp in self.products_graph.nodes:
                if p != pp:  # controllo solo i nodi diversi
                    peso = DAO.get_n_sales(p, pp, year)
                    if peso > 0:  #controllo sia stato venduto da almeno due
                        self.products_graph.add_edge(p, pp, weight=peso)
        self.check_max()

    def check_max(self):
        """
        Scandisce gli archi e vede quelli con peso maggiore
        """
        for arco in self.products_graph.edges.data():
            if len(self.max_weight) < 3:
                self.max_weight.append(arco)
            else:
                arco_min = min(self.max_weight, key=lambda x: x[2]["weight"])  #estraggo l'arco di peso minimo
                if arco[2]["weight"] > arco_min[2]["weight"]:  #solo se il peso è maggiore di quello trovato
                    self.max_weight.append(arco)
                    self.max_weight.remove(arco_min)
        self.check_duplicati()

    def check_duplicati(self):
        """
        Controlla la presenza di duplicati nella lista dei massimi (doppio for sugli archi)
        """
        for arco in self.max_weight:
            for arco2 in self.max_weight:
                if arco != arco2:
                    if arco[0] == arco2[0]:
                        self.duplicati.add(arco[0])
                    elif arco[1] == arco2[1]:
                        self.duplicati.add(arco[1])
                    elif arco[0] == arco2[1]:
                        self.duplicati.add(arco[1])
                    elif arco[1] == arco2[0]:
                        self.duplicati.add(arco[1])
        self.duplicati = list(self.duplicati)  #creo una lista dall'insieme per la stampa

    def num_nodes(self):
        return len(self.products_graph.nodes)

    def num_edges(self):
        return len(self.products_graph.edges)

    def get_percorso(self, v0):
        self.ricorsione(v0, [], [0])

    def ricorsione(self, source, parziale, pesi_max):
        if len(parziale) > len(self.soluzione):
            self.soluzione = copy.deepcopy(parziale)
            print(parziale)
        for neighbor in self.products_graph.neighbors(source):
            peso = self.products_graph[source][neighbor]["weight"]
            if self.check(neighbor, source, parziale) and peso >= pesi_max[len(parziale)]:
                pesi_max.append(peso)
                parziale.append((neighbor, source))
                self.ricorsione(neighbor, parziale, pesi_max)
                parziale.pop()
                pesi_max.pop()

    def check(self, neighbor, prec, parziale):
        for tupla in parziale:
            if (tupla[0] == neighbor and tupla[1] == prec) or (
                    tupla[0] == prec and tupla[1] == neighbor) or neighbor == prec:
                return False
        return True
