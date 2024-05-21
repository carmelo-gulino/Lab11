import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.products = DAO.get_all_products()
        self.sales = DAO.get_all_sales()
        self.products_map = {}
        for p in self.products:
            self.products_map[p.Product_number] = p
        self.products_graph = nx.Graph()

    def build_graph(self, year, color):
        self.products_graph.clear_edges()
        for p in self.products:  # scandisco i prodotti e aggiungo il nodo se il colore corrisponde
            if p.Product_color == color:
                self.products_graph.add_node(p)
        for p in self.products_graph.nodes:
            for pp in self.products_graph.nodes:
                if p!= pp:  # controllo solo i nodi diversi
                    if DAO.get_n_sales(p, pp, year):
                        self.products_graph.add_edge(p, pp)
                        print("Added edge")

    def num_nodes(self):
        return len(self.products_graph.nodes)

    def num_edges(self):
        return len(self.products_graph.edges)
