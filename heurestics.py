# heuristics.py

# heuristics based on D1 idea (MST + nearest node, simplified)

from graph import GRAPH


# shortest distance using BFS (simple version)
def shortest_dist(start, goal):
    from collections import deque

    queue = deque([(start, 0)])
    visited = set()

    while queue:
        node, dist = queue.popleft()

        if node == goal:
            return dist

        if node in visited:
            continue

        visited.add(node)

        for neigh, _ in GRAPH[node]:
            queue.append((neigh, dist + 1))

    return 0


# heuristic 1: MST-like idea (connect all remaining nodes)
def h1(state, problem):
    nodes = set()
    nodes.add(state.pos)

    for idx in state.pending_pickups:
        order = problem.order_map[idx]
        nodes.add(order.pickup)
        nodes.add(order.delivery)

    for idx in state.pending_deliveries:
        order = problem.order_map[idx]
        nodes.add(order.delivery)

    nodes = list(nodes)

    if len(nodes) <= 1:
        return 0

    visited = {nodes[0]}
    cost = 0

    while len(visited) < len(nodes):
        best = float('inf')
        next_node = None

        for u in visited:
            for v in nodes:
                if v not in visited:
                    d = shortest_dist(u, v)
                    if d < best:
                        best = d
                        next_node = v

        cost += best
        visited.add(next_node)

    return cost


# heuristic 2: nearest node
def h2(state, problem):
    current = state.pos
    targets = []

    for idx in state.pending_pickups:
        targets.append(problem.order_map[idx].pickup)

    for idx in state.pending_deliveries:
        targets.append(problem.order_map[idx].delivery)

    if not targets:
        return 0

    return min(shortest_dist(current, t) for t in targets)


# final heuristic
def heuristic(state, problem):
    return max(h1(state, problem), h2(state, problem))