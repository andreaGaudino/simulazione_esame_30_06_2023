import copy
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

    def graphDetails(self):
        return len(self.graph.nodes), len(self.graph.edges)







