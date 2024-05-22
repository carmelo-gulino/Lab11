import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.products = DAO.get_all_products()
        self.products_map = {}
        for p in self.products:
            self.products_map[p.Product_number] = p
        self.products_graph = nx.Graph()
        self.max_weight = []
        self.duplicati = set()
        self.soluzioni = []
        self.sol_best = None

    def build_graph(self, year, color):
        self.max_weight = []  #resetto la lista dei max
        self.duplicati = set()  #resetto l'insieme dei duplicati
        self.products_graph.clear()  #resetto il grafo
        for p in self.products:  # scandisco i prodotti e aggiungo il nodo se il colore corrisponde
            if p.Product_color == color:
                self.products_graph.add_node(p)
        for p in self.products_graph.nodes:
            for pp in self.products_graph.nodes:
                if p != pp:  # controllo solo i nodi diversi
                    peso = DAO.get_n_sales(p, pp, year)
                    if peso > 0:  #controllo sia stato venduto da almeno due
                        self.products_graph.add_edge(p, pp, weight=peso)
        self.check_max()

    def check_max(self):
        """
        Scandisce gli archi e vede quelli con peso maggiore, facendo attenzione ai duplicati
        """
        for arco in self.products_graph.edges.data():
            if len(self.max_weight) < 3:
                self.max_weight.append(arco)
            else:
                arco_min = min(self.max_weight, key=lambda x: x[2]["weight"])
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
        self.duplicati = list(self.duplicati)  #creo una lista dall'insieme per la stampa

    def num_nodes(self):
        return len(self.products_graph.nodes)

    def num_edges(self):
        return len(self.products_graph.edges)

    def get_percorso(self, v0):
        self.ricorsione(v0, v0, set())

    def ricorsione(self, nodo, prec, parziale):
        for neighbor in self.products_graph[nodo]:  #guardo tutti i vicini del nodo
            if len(self.products_graph[nodo]) == 1:   #se ho un solo vicino
                vicino = self.products_graph[nodo][0]
                if vicino == prec:  # se il vicino è uguale al precedente, ho trovato una soluzione
                    self.soluzioni.append(copy.deepcopy(parziale))  #aggiungo alla lista di soluzioni
            else:
                parziale.add(neighbor)
                prec = neighbor
                self.ricorsione(nodo, prec, parziale)

