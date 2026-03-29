# graph.py

# simple graph for campus map
# nodes = 1 to 26

NODE_NAMES = {
    1: "SR",
    2: "Workshop",
    3: "Library",
    4: "Food",
    5: "LTC",
    6: "FD3",
    7: "FD2",
    8: "FD1",
    9: "Malviya",
    10: "Looters",
    11: "Dominos",
    12: "Ram",
    13: "Krishna",
    14: "VK",
    15: "RP",
    16: "CVR",
    17: "Budh",
    18: "Gandhi",
    19: "Bhagirath",
    20: "Ashok",
    21: "Gate",
    22: "Shankar",
    23: "ANC",
    24: "Meera",
    25: "Vyas",
    26: "CNOT"
}

# edges (u, v, distance)
EDGES = [
    (1,2,300),(2,3,100),(2,4,20),(4,5,150),(4,8,50),
    (6,7,250),(6,12,160),(7,8,250),(7,13,160),
    (8,14,350),(8,15,300),
    (9,10,100),(9,11,70),(9,12,230),
    (10,17,230),(10,24,750),
    (11,17,190),(11,12,70),
    (12,13,400),
    (13,14,230),(13,18,200),
    (14,15,270),(14,19,200),
    (15,16,30),(15,20,190),
    (16,20,30),(16,21,150),
    (17,18,260),
    (18,19,220),(18,22,140),
    (19,20,250),(19,23,150),
    (20,23,240),(20,21,300),
    (21,26,700),
    (22,23,180),(22,25,190),
    (23,26,800),
    (24,25,400),(24,26,900),
    (25,26,600)
]

# build graph
GRAPH = {}
for i in range(1, 27):
    GRAPH[i] = []

for u, v, w in EDGES:
    GRAPH[u].append((v, w))
    GRAPH[v].append((u, w))


def node_name(n):
    return NODE_NAMES.get(n, str(n))


def path_to_names(path):
    return " -> ".join(node_name(x) for x in path)