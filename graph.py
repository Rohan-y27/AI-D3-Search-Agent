# graph.py - BITS Pilani campus graph
# nodes and edges taken from our D1 submission map
# using 0-indexed node IDs (N1 in report = index 0 here)

INF = float('inf')

node_names = {
    0: "SR Bhawan", 1: "Workshop", 2: "Library", 3: "Food Ministry",
    4: "LTC", 5: "FD3", 6: "FD2", 7: "FD1",
    8: "Malviya Bhawan", 9: "Looters/301", 10: "Dominos",
    11: "Ram Bhawan", 12: "Krishna Bhawan", 13: "VK Bhawan",
    14: "RP Bhawan", 15: "CVR Bhawan", 16: "Budh Bhawan",
    17: "Gandhi Bhawan", 18: "Bhagirath Bhawan", 19: "Ashok Bhawan",
    20: "Main Gate", 21: "Shankar Bhawan", 22: "ANC",
    23: "Meera Bhawan", 24: "Vyas Bhawan", 25: "C'not"
}

# short labels for printing paths
short = {
    0: "SR", 1: "WS", 2: "LIB", 3: "FM", 4: "LTC",
    5: "FD3", 6: "FD2", 7: "FD1", 8: "MAL", 9: "LOT",
    10: "DOM", 11: "RAM", 12: "KRI", 13: "VK", 14: "RP",
    15: "CVR", 16: "BDH", 17: "GAN", 18: "BHG", 19: "ASH",
    20: "GATE", 21: "SHK", 22: "ANC", 23: "MRA", 24: "VYS",
    25: "CNOT"
}

# which nodes are pickup spots vs delivery spots
pickup_nodes = {3, 9, 10, 22, 25}  # FM, Looters, Dominos, ANC, Cnot
# everything else is a delivery/dropoff node

# edge list from D1 report page 14
# format: (nodeA, nodeB, distance in metres)
# N1=0, N2=1, ... N26=25
edges_list = [
    (0, 1, 300),    # SR - WS
    (1, 2, 100),    # WS - LIB
    (1, 3, 20),     # WS - FM (shortest edge on campus lol)
    (3, 4, 150),    # FM - LTC
    (3, 7, 50),     # FM - FD1
    (5, 6, 250),    # FD3 - FD2
    (5, 11, 160),   # FD3 - Ram
    (6, 7, 250),    # FD2 - FD1
    (6, 12, 160),   # FD2 - Krishna
    (7, 13, 350),   # FD1 - VK
    (7, 14, 300),   # FD1 - RP
    (8, 9, 100),    # Malviya - Looters
    (8, 10, 70),    # Malviya - Dominos
    (8, 11, 230),   # Malviya - Ram
    (9, 16, 230),   # Looters - Budh
    (9, 23, 750),   # Looters - Meera (long edge)
    (10, 16, 190),  # Dominos - Budh
    (10, 11, 70),   # Dominos - Ram
    (11, 12, 400),  # Ram - Krishna
    (12, 13, 230),  # Krishna - VK
    (12, 17, 200),  # Krishna - Gandhi
    (13, 14, 270),  # VK - RP
    (13, 18, 200),  # VK - Bhagirath
    (14, 19, 190),  # RP - Ashok
    (14, 15, 30),   # RP - CVR
    (15, 19, 30),   # CVR - Ashok
    (15, 20, 150),  # CVR - Main Gate
    (16, 17, 260),  # Budh - Gandhi
    (17, 18, 220),  # Gandhi - Bhagirath
    (17, 21, 140),  # Gandhi - Shankar
    (18, 19, 250),  # Bhagirath - Ashok
    (18, 22, 150),  # Bhagirath - ANC
    (19, 22, 240),  # Ashok - ANC
    (19, 20, 300),  # Ashok - Gate
    (20, 25, 700),  # Gate - Cnot
    (21, 22, 180),  # Shankar - ANC
    (21, 24, 190),  # Shankar - Vyas
    (22, 25, 800),  # ANC - Cnot (longest path through here)
    (23, 24, 400),  # Meera - Vyas
    (23, 25, 900),  # Meera - Cnot (longest edge)
    (24, 25, 600),  # Vyas - Cnot
]

NUM_NODES = 26

# positions for drawing the graph (eyeballed from campus map)
positions = {
    0: (350, 30), 1: (300, 130), 2: (400, 130), 3: (280, 160),
    4: (480, 140), 5: (160, 220), 6: (300, 230), 7: (420, 230),
    8: (120, 280), 9: (80, 310), 10: (50, 340), 11: (130, 340),
    12: (320, 340), 13: (440, 310), 14: (530, 280), 15: (570, 310),
    16: (200, 380), 17: (320, 410), 18: (410, 380), 19: (500, 370),
    20: (620, 370), 21: (290, 470), 22: (380, 450), 23: (150, 510),
    24: (270, 530), 25: (450, 570),
}


class Graph:
    def __init__(self):
        self.n = NUM_NODES
        # adjacency list
        self.adj = [[] for _ in range(NUM_NODES)]
        for u, v, w in edges_list:
            self.adj[u].append((v, w))
            self.adj[v].append((u, w))

        # precompute all pairs shortest paths
        # using floyd warshall (|V|^3 = 26^3 = 17576, basically instant)
        self.sp = self._run_floyd_warshall()

    def _run_floyd_warshall(self):
        n = self.n
        d = [[INF]*n for _ in range(n)]
        for i in range(n):
            d[i][i] = 0
        for u, v, w in edges_list:
            if w < d[u][v]:  # handle parallel edges just in case
                d[u][v] = w
                d[v][u] = w

        for k in range(n):
            dk = d[k]
            for i in range(n):
                if d[i][k] >= INF:
                    continue
                dik = d[i][k]
                di = d[i]
                for j in range(n):
                    newdist = dik + dk[j]
                    if newdist < di[j]:
                        di[j] = newdist
        return d

    def get_neighbors(self, v):
        return self.adj[v]

    def shortest_dist(self, u, v):
        return self.sp[u][v]
