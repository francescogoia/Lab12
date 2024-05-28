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
                            self._grafo.add_edge(self._idMap[a["R1"]], self._idMap[a["R2"]], weight=a["NumProdInComune"])

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
      #  print(list_comp_conn)
        self._best_soluzione = []
        for c in list_comp_conn:
            if len(c) > 1:
                n = list(c)[0]
                self._ricorsione(n, [], 0)

        print(self._best_soluzione)


    def _ricorsione(self, nodo, parziale, peso_parziale):
        if len(parziale) > self._num_archi:
            return
        if len(parziale) > 2:
            if parziale[0][0] == parziale[-1][0]:
                if len(parziale) == self._num_archi and peso_parziale > self._pesoMax:
                    self._best_soluzione.append(copy.deepcopy(parziale))
        vicini = self._grafo.neighbors(nodo)
        for v in vicini:
            peso_arco = self._grafo[nodo][v]["weight"]
            if len(parziale) == self._num_archi - 1:
                if self.filtro(nodo, v, parziale) == True and peso_parziale + peso_arco >= self._pesoMax:
                    peso_parziale += peso_arco
                    parziale.append((nodo, v, peso_parziale))
                    self._ricorsione(nodo, parziale, peso_parziale)
                    parziale.pop()
            else:          # il primo nodo deve essere uguale all'ultimo (è un ciclo)
                parziale.append((nodo, v, peso_parziale))
                self._ricorsione(nodo, parziale, peso_parziale)
                parziale.pop()


    def filtro(self, nodo, n, parziale):
        for arco in parziale:
            if arco[:2] == (nodo, n) or arco[:2] == (n, nodo):  ## se i nodi dell'arco sono quelli passati return True (se parziale contiene già i nodi passati --> False)
                return False
        return True





    def info_grafo(self):
        return f"Il grafo ha {len(self._grafo.nodes)} nodi e {len(self._grafo.edges)} archi"