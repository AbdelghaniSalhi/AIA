from collections import namedtuple, deque
from pprint import pprint as pp
import pandas as pd

inf = float('inf')

# Cette structure nous permettra de créer notre graphe
Arrete = namedtuple('Arrete', ['origine', 'dest', 'cout'])

class Graph():
    def __init__(self, arretes):
        self.arretes = [Arrete(*arrete) for arrete in arretes]
        self.sommets = {e.origine for e in self.arretes} | {e.dest for e in self.arretes}

    def dijkstra(self, source, fin):

        # On verifie que notre station appartient bien a l'ensemble
        # de nos Sommets
        assert source in self.sommets, "Le sommet de départ renseigné n'existe pas"
        assert fin in self.sommets, "Le sommet d'arrivée renseigné n'existe pas"

        dist = {sommet: inf for sommet in self.sommets}
        precedent = {sommet: None for sommet in self.sommets}
        dist[source] = 0
        q = self.sommets.copy()
        voisins = {sommet: set() for sommet in self.sommets}

        # On crée une liste d'adjacence pour chaque sommet
        for origine, dest, cout in self.arretes:
            voisins[origine].add((dest, cout))
        while q:
            u = min(q, key=lambda sommet: dist[sommet])
            q.remove(u)
            if dist[u] == inf or u == fin:
                break
            for v, cout in voisins[u]:
                alt = dist[u] + cout
                if alt < dist[v]:
                    dist[v] = alt
                    precedent[v] = u
        s, u = deque(), fin
        while precedent[u]:
            s.appendleft(u)
            u = precedent[u]
        s.appendleft(u)
        return s

def graph_generator(file):
    # Lecture du fichier de trajets
    df = pd.read_csv(file, sep='\t', usecols=['trajet','duree'])
    # Les lignes nan sont intraitables et donc supprimées du dataframe
    df.dropna()
    # Structure de retour finale
    res = []
    # On parcourt les rows(lignes) du dataframe
    for ind, row in df.iterrows():
        # La colonne trajet contient le départ et la destination
        # On récupere donc séparemment chaque gare en splittant
        # le contenu de la colonne
        res.append((row['trajet'].split(' - ')[0],
                    row['trajet'].split(' - ')[1],
                    int(row['duree'])))
        # Le graphe construit est ORIENTE
        # Comme la durée entre deux gares ne change pas
        # a l'aller et au retour, on ajoute les deux
        # Durée ST-Lazare/Lyon = Durée Lyon/ST-Lazare
        res.append((row['trajet'].split(' - ')[1],
                    row['trajet'].split(' - ')[0],
                    int(row['duree'])))
    # On retourne une liste de tuples de la forme
    # ("Gare de départ", "Gare d'arrivee", durée)
    return res

# On génere notre structure
graphe = graph_generator('venv/data/timetables.csv')

# On coonstruit notre graphe grâce à notre structure
graph = Graph(graphe)

# Quelques tests unitaires
pp(graph.dijkstra("Gare de Paris-St-Lazare", "Gare de Compiègne"))

graph = Graph([("a", "b", 7),  ("a", "c", 9),  ("a", "f", 14), ("b", "c", 10),
               ("b", "d", 15), ("c", "d", 11), ("c", "f", 2),  ("d", "e", 6),
               ("e", "f", 9)])
pp(graph.dijkstra("a", "e"))