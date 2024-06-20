import copy
import random
from math import sqrt
#from geopy.distance import geodesic

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):

        self.graph = nx.Graph()


    def getTeams(self):
        squadre = DAO.getAllTeams()
        return squadre

    def buildGraph(self, team):
        self.graph.clear()
        anni = DAO.getNodes(team)
        self.graph.add_nodes_from(anni)

        for i in DAO.getEdges(team):
            self.graph.add_edge(i[0], i[1], weight = i[2])
        for v in anni:
            for u in anni:
                if not self.graph.has_edge(v, u):
                    self.graph.add_edge(v, u, weight = 0)

    def getDettagli(self, anno):
        vicini = list(self.graph.neighbors(anno))
        result = {}
        for v in vicini:
            result[v] = self.graph[anno][v]["weight"]
        sortedResult = sorted(result, key = lambda x: result[x], reverse=True)
        final = {}
        for k in sortedResult:
            final[k] = result[k]
        return final


    def simulazione(self, tifosi, anno, squadra):
        tifosiPersi = 0
        dizio = DAO.getPlayers(squadra, anno)
        #condizioni iniziali
        giocatoriAnnoPrecedente = dizio[anno]
        numGiocatori = len(giocatoriAnnoPrecedente)
        tifosiPlayer = {}
        for player in giocatoriAnnoPrecedente:
            tifosiPlayer[player] = round(tifosi/numGiocatori)
        dizio.pop(anno)
        for year in dizio:
            giocatoriAttuali = dizio[year]
            for g in giocatoriAnnoPrecedente:
                if g in giocatoriAttuali:
                    tif = tifosiPlayer[g]
                    tifosiPlayer[g] = round(tif*0.9)
                    giocatore = g
                    while giocatore == g:
                        giocatore = random.choice(giocatoriAttuali)
                    if giocatore not in tifosiPlayer:
                        tifosiPlayer[giocatore] = round(0.1*tif)
                    else:
                        tifosiPlayer[giocatore] += round(0.1 * tif)
                    #giocatoriAnnoPrecedente = giocatoriAttuali
                else:
                    tifosiPersi += round(tifosiPlayer[g]*0.1)
                    tifosiNuovi = round(tifosiPlayer[g]*0.9)
                    tifosiPlayer[g] = 0
                    giocatoriNuovi = [e for e in giocatoriAttuali if e not in giocatoriAnnoPrecedente]
                    giocatoriGiaPresenti = [item for item in giocatoriAttuali if item in giocatoriAnnoPrecedente]
                    percentage = random.random()
                    if percentage< 0.75:
                        giocatoreRandom = random.choice(giocatoriNuovi)
                        tifosiPlayer[giocatoreRandom] = tifosiNuovi
                    else:
                        giocatoreRandom = random.choice(giocatoriGiaPresenti)
                        tifosiPlayer[giocatoreRandom] += tifosiNuovi
            giocatoriAnnoPrecedente = copy.deepcopy(giocatoriAttuali)

        return tifosiPlayer, tifosiPersi








    def graphDetails(self):
        return len(self.graph.nodes), len(self.graph.edges)







