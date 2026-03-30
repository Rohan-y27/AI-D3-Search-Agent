# orders.py
# handles order definitions, state transitions, and the two heuristics from D1
#
# state is a tuple: (current_node, pickup_mask, delivery_mask)
# masks are bitmasks - bit i is 1 if order i is still pending
# eg for K=4 orders, initial mask = 0b1111 = 15

import heapq
from graph import Graph

# ---- order class ----

class Order:
    def __init__(self, pickup, delivery):
        self.pickup = pickup
        self.delivery = delivery

    def __repr__(self):
        return f"Order({self.pickup}->{self.delivery})"


# ---- test cases ----
# tried to pick orders that test different parts of the campus

def get_easy():
    # K=2, nearby orders
    return [
        Order(3, 11),   # FM -> Ram Bhawan
        Order(10, 16),  # Dominos -> Budh
    ]

def get_medium():
    # K=4, spread across campus
    return [
        Order(3, 0),    # FM -> SR
        Order(10, 17),  # Dominos -> Gandhi
        Order(22, 13),  # ANC -> VK
        Order(9, 19),   # Looters -> Ashok
    ]

def get_hard():
    # K=6, really spread out, includes C'not which is far from everything
    return [
        Order(3, 11),   # FM -> Ram
        Order(10, 0),   # Dominos -> SR
        Order(22, 13),  # ANC -> VK
        Order(9, 18),   # Looters -> Bhagirath
        Order(25, 14),  # C'not -> RP
        Order(3, 24),   # FM -> Vyas
    ]


# ---- state transition logic ----

def apply_effects(node, pr, dr, orders):
    """when agent reaches a node, auto-complete any pickups/deliveries there"""
    # first do pickups
    for i in range(len(orders)):
        mask = 1 << i
        if orders[i].pickup == node and (pr & mask):
            pr = pr ^ mask  # flip bit off

    # then deliveries (only if pickup already done)
    for i in range(len(orders)):
        mask = 1 << i
        if orders[i].delivery == node and (dr & mask) and not (pr & mask):
            dr = dr ^ mask

    return pr, dr


def successors(state, graph, orders):
    """get all next states from current state by moving to adjacent nodes"""
    v, pr, dr = state
    result = []
    for neighbor, weight in graph.get_neighbors(v):
        new_pr, new_dr = apply_effects(neighbor, pr, dr, orders)
        result.append(((neighbor, new_pr, new_dr), weight))
    return result


def check_goal(state, end_node=None):
    """check if we've completed all orders (and optionally reached end node)"""
    v, pr, dr = state
    if pr != 0 or dr != 0:
        return False
    if end_node is not None and v != end_node:
        return False
    return True


def init_state(start, orders):
    """create the starting state"""
    k = len(orders)
    all_bits = (1 << k) - 1
    # apply effects at start node (in case start is a pickup/delivery location)
    pr, dr = apply_effects(start, all_bits, all_bits, orders)
    return (start, pr, dr)


# ---- heuristics ----
# h1 = MST based (from D1 section 4.1)
# h2 = min-edge based (from D1 section 4.2)
# both proved admissible and consistent in D1

def _get_task_nodes(state, orders, dest):
    """figure out which nodes we still need to visit"""
    v, pr, dr = state
    nodes = set()
    nodes.add(v)
    for i in range(len(orders)):
        if pr & (1 << i):
            nodes.add(orders[i].pickup)
        if dr & (1 << i):
            nodes.add(orders[i].delivery)
    if dest is not None:
        nodes.add(dest)
    return list(nodes)


def _mst_cost(nodes, graph):
    """prim's MST on the complete graph over nodes[] using shortest path weights"""
    if len(nodes) <= 1:
        return 0

    n = len(nodes)
    visited = [False] * n
    cheapest = [float('inf')] * n
    cheapest[0] = 0
    total = 0
    pq = [(0, 0)]
    count = 0

    while pq and count < n:
        cost, idx = heapq.heappop(pq)
        if visited[idx]:
            continue
        visited[idx] = True
        total += cost
        count += 1
        u_node = nodes[idx]
        for j in range(n):
            if not visited[j]:
                d = graph.shortest_dist(u_node, nodes[j])
                if d < cheapest[j]:
                    cheapest[j] = d
                    heapq.heappush(pq, (d, j))
    return total


def h1(state, graph, orders, dest):
    """MST heuristic - lower bound because optimal route spans all task nodes"""
    v, pr, dr = state
    if pr == 0 and dr == 0:
        if dest is not None:
            return graph.shortest_dist(v, dest)
        return 0

    nodes = _get_task_nodes(state, orders, dest)
    return _mst_cost(nodes, graph)


def h2(state, graph, orders, dest):
    """min-edge heuristic - for each remaining node, cheapest edge to another"""
    v, pr, dr = state
    if pr == 0 and dr == 0:
        if dest is not None:
            return graph.shortest_dist(v, dest)
        return 0

    nodes = _get_task_nodes(state, orders, dest)
    task_only = [x for x in nodes if x != v]
    if len(task_only) == 0:
        return 0

    # lb1: how far to nearest task node
    lb1 = min(graph.shortest_dist(v, t) for t in task_only)

    # lb2: sum of min edges, halved (each edge counted twice)
    total = 0
    for u in nodes:
        best = float('inf')
        for w in nodes:
            if w != u:
                d = graph.shortest_dist(u, w)
                if d < best:
                    best = d
        if best < float('inf'):
            total += best
    lb2 = (total + 1) // 2  # ceiling division

    return max(lb1, lb2)


def combined_h(state, graph, orders, dest):
    """max of both heuristics - still admissible since both are LBs"""
    return max(h1(state, graph, orders, dest), h2(state, graph, orders, dest))
