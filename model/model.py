import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._num_archi = 0
        self._list_countries = DAO.get_all_countries()
        self._list_retailers = []
        self._grafo = nx.Graph()
        self._idMap = {}

    def build_graph(self, country, anno):
        self._list_retailers = DAO.get_reatiler_country(country)
        for r in self._list_retailers:
            self._idMap[r.Retailer_code] = r
        self._grafo.add_nodes_from(self._list_retailers)
        for r1 in self._grafo.nodes:
            for r2 in self._grafo.nodes:
                if r1 != r2:
                    archi = DAO.get_archi(r1.Retailer_code, r2.Retailer_code, anno)
                    if len(archi) != 0:
                        for a in archi:
                            self._grafo.add_edge(self._idMap[a["R1"]], self._idMap[a["R2"]],
                                                 weight=a["NumProdInComune"])

    def calcola_volumi(self):
        for retailer in self._grafo.nodes:
            vicini = self._grafo.neighbors(retailer)
            retailer.initialize_volume()
            for v in vicini:
                peso = self._grafo[retailer][v]["weight"]
                retailer.add_volume(peso)

    def ordina_retailer_per_volume(self):
        copia_retailer = copy.deepcopy(self._list_retailers)
        copia_retailer.sort(key=lambda x: x.volume, reverse=True)
        return copia_retailer

    def calcola_percorso(self, numArchi):
        self._num_archi = numArchi

        self._pesoMax = 0

        comp_conn = nx.connected_components(self._grafo)
        list_comp_conn = list(comp_conn)
        # print(list_comp_conn)
        self._best_soluzione = []
        for c in list_comp_conn:
            # print(list(c))
            if len(c) > 2:
                for n in c:
                    self._ricorsione(n, [], 0)
                # chiamo la ricorsione per tutte le componenti connesse con lunghezza maggiore di 2 (almeno 2 archi)

        print(self._best_soluzione)
        print(self._pesoMax)
        return self._pesoMax, self._best_soluzione

    def _ricorsione(self, nodo, parziale, peso_parziale):
        # ho già controllato che len parziale non superi num_archi
        if len(parziale) == self._num_archi:
            if parziale[0][0] == parziale[-1][1] and peso_parziale > self._pesoMax:
                print(f"Found a valid cycle with new max weight: {peso_parziale} -> {parziale}")
                self._pesoMax = peso_parziale
                self._best_soluzione = copy.deepcopy(parziale)
        vicini = self._grafo.neighbors(nodo)
        for v in vicini:
            peso_arco = self._grafo[nodo][v]["weight"]
        #    if peso_parziale + peso_arco > self._pesoMax:      # è sbagliato controllare già qui pesoMax (parziale è più corto di quanto deve essere)
            if len(parziale) < self._num_archi:
                    if self.filtro(v, parziale):
                        parziale.append((nodo, v, peso_arco))  # in parziale metto l'arco: (u, v, peso)
                        self._ricorsione(v, parziale, peso_parziale + peso_arco)
                        parziale.pop()
            if len(parziale) == self._num_archi - 1:  # il primo nodo deve essere uguale all'ultimo (è un ciclo) quindi non passo dal filtro
                if peso_parziale + peso_arco > self._pesoMax:
                    parziale.append((nodo, v, peso_parziale))
                    if parziale[0][0] == parziale[-1][1]:
                        self._ricorsione(nodo, parziale, peso_parziale + peso_arco)
                    parziale.pop()

    def filtro(self, nodo, parziale):
        for arco in parziale:
            if arco[0] == nodo or arco[1] == nodo:
                ## se un nodo dell'arco non è quello passato return True (se parziale contiene già un nodo passato --> False)
                return False
        return True

    def info_grafo(self):
        return f"Il grafo ha {len(self._grafo.nodes)} nodi e {len(self._grafo.edges)} archi"
