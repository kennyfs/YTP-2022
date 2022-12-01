import matplotlib.pyplot as plt
import networkx as nx

class Graph:
    def __init__(self):
        self.cnt = 0
        self.E = []
        self.S = {}
        self.P = {}
        self.W = []
    def setSize(self, u, s):
        self.S[u] = s
    def addEdge(self, u, v):
        if(v < u):
            u, v = v, u
        if(self.P.get((u, v))):
            self.W[self.P[(u, v)]] += 1
        else:
            self.W.append(1)
            self.E.append([u, v])
            self.P[(u, v)] = self.cnt
            self.cnt += 1
    def saveAsImage(self, filename='DGWang.jpg'):
        G = nx.Graph()
        for i in range(0, len(self.E)):
            G.add_edge(self.E[i][0], self.E[i][1], weight = self.W[i])
        way = nx.spring_layout(G)
        wid = nx.get_edge_attributes(G, 'weight').values()
        nx.draw_networkx(G, pos = way, font_size = 20, font_color = 'grey', node_shape = 'o', node_color = 'skyblue', node_size = [s * 100 for s in self.S.values()], alpha = 0.8, edge_color ='grey', width = list(wid))
        plt.savefig(filename)
if __name__=='__main__':
    G = Graph()
    G.setSize(1, 2), G.setSize(2, 4), G.setSize(3, 6), G.setSize(4, 4)
    G.addEdge(1, 2), G.addEdge(2, 3), G.addEdge(3, 1), G.addEdge(3, 1), G.addEdge(3, 1), G.addEdge(1, 3), G.addEdge(1, 4), G.addEdge(2, 4)
    G.saveAsImage()
