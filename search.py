# search.py
# implementations of BFS, DFS, A*, IDA* for the campus delivery problem
# each function returns a dict with path, cost, stats etc

import heapq
import time
import sys
from collections import deque
from graph import Graph
from orders import (Order, successors, check_goal, init_state,
                    combined_h, h1, h2)


def trace_path(parents, goal_state):
    """backtrack through parent pointers to get the path"""
    path = []
    cur = goal_state
    while cur is not None:
        path.append(cur[0])  # just the node index
        cur = parents.get(cur)
    path.reverse()
    return path


def calc_path_cost(path, graph):
    """add up edge weights along a path"""
    cost = 0
    for i in range(len(path) - 1):
        for nb, w in graph.get_neighbors(path[i]):
            if nb == path[i+1]:
                cost += w
                break
    return cost


# ====================== BFS ======================
# finds min-hop path, NOT min-cost (since edges have different weights)

def run_bfs(graph, orders, start, dest=None):
    t_start = time.perf_counter()
    s0 = init_state(start, orders)

    if check_goal(s0, dest):
        return {"algo": "BFS", "path": [start], "cost": 0,
                "expanded": 0, "generated": 1, "frontier_max": 1,
                "time_ms": 0, "trace": [s0]}

    queue = deque()
    queue.append((s0, 0))
    visited = {s0: 0}
    parents = {s0: None}
    expanded = 0
    generated = 1
    max_q = 1
    exploration = []

    while queue:
        state, g = queue.popleft()
        expanded += 1
        exploration.append(state)

        for next_state, step_cost in successors(state, graph, orders):
            ng = g + step_cost

            # only explore if we havent seen this state or found cheaper path
            if next_state not in visited or ng < visited[next_state]:
                visited[next_state] = ng
                parents[next_state] = state
                generated += 1

                if check_goal(next_state, dest):
                    elapsed = (time.perf_counter() - t_start) * 1000
                    p = trace_path(parents, next_state)
                    return {"algo": "BFS", "path": p, "cost": ng,
                            "expanded": expanded, "generated": generated,
                            "frontier_max": max_q, "time_ms": round(elapsed, 2),
                            "trace": exploration}

                queue.append((next_state, ng))
                if len(queue) > max_q:
                    max_q = len(queue)

    elapsed = (time.perf_counter() - t_start) * 1000
    return {"algo": "BFS", "path": [], "cost": -1,
            "expanded": expanded, "generated": generated,
            "frontier_max": max_q, "time_ms": round(elapsed, 2),
            "trace": exploration}


# ====================== DFS ======================
# explores depth-first, returns first complete path found
# uses explored set to avoid infinite loops

def run_dfs(graph, orders, start, dest=None):
    t_start = time.perf_counter()
    s0 = init_state(start, orders)

    if check_goal(s0, dest):
        return {"algo": "DFS", "path": [start], "cost": 0,
                "expanded": 0, "generated": 1, "frontier_max": 1,
                "time_ms": 0, "trace": [s0]}

    stack = [(s0, 0)]
    seen = set()
    parents = {s0: None}
    costs = {s0: 0}
    expanded = 0
    generated = 1
    max_stk = 1
    exploration = []

    while stack:
        state, g = stack.pop()

        if state in seen:
            continue
        seen.add(state)
        expanded += 1
        exploration.append(state)

        if check_goal(state, dest):
            elapsed = (time.perf_counter() - t_start) * 1000
            p = trace_path(parents, state)
            return {"algo": "DFS", "path": p, "cost": g,
                    "expanded": expanded, "generated": generated,
                    "frontier_max": max_stk, "time_ms": round(elapsed, 2),
                    "trace": exploration}

        for next_state, step_cost in successors(state, graph, orders):
            if next_state not in seen:
                ng = g + step_cost
                if next_state not in costs or ng < costs[next_state]:
                    costs[next_state] = ng
                    parents[next_state] = state
                generated += 1
                stack.append((next_state, costs[next_state]))
                if len(stack) > max_stk:
                    max_stk = len(stack)

    elapsed = (time.perf_counter() - t_start) * 1000
    return {"algo": "DFS", "path": [], "cost": -1,
            "expanded": expanded, "generated": generated,
            "frontier_max": max_stk, "time_ms": round(elapsed, 2),
            "trace": exploration}


# ====================== A* ======================
# uses combined heuristic h = max(h1_mst, h2_min_edge)
# guaranteed optimal since h is consistent (proved in D1)

def run_astar(graph, orders, start, dest=None):
    t_start = time.perf_counter()
    s0 = init_state(start, orders)
    h0 = combined_h(s0, graph, orders, dest)

    # pq entries: (f_value, tiebreaker, state, g_value)
    # tiebreaker needed because tuples cant compare states
    counter = 0
    pq = [(h0, counter, s0, 0)]
    best_g = {s0: 0}
    parents = {s0: None}
    expanded = 0
    generated = 1
    max_pq = 1
    exploration = []

    while pq:
        f, _, state, g = heapq.heappop(pq)

        # skip stale entries
        if g > best_g.get(state, float('inf')):
            continue

        expanded += 1
        exploration.append(state)

        if check_goal(state, dest):
            elapsed = (time.perf_counter() - t_start) * 1000
            p = trace_path(parents, state)
            return {"algo": "A*", "path": p, "cost": g,
                    "expanded": expanded, "generated": generated,
                    "frontier_max": max_pq, "time_ms": round(elapsed, 2),
                    "trace": exploration}

        for next_state, step_cost in successors(state, graph, orders):
            ng = g + step_cost
            if ng < best_g.get(next_state, float('inf')):
                best_g[next_state] = ng
                h = combined_h(next_state, graph, orders, dest)
                counter += 1
                heapq.heappush(pq, (ng + h, counter, next_state, ng))
                parents[next_state] = state
                generated += 1
                if len(pq) > max_pq:
                    max_pq = len(pq)

    elapsed = (time.perf_counter() - t_start) * 1000
    return {"algo": "A*", "path": [], "cost": -1,
            "expanded": expanded, "generated": generated,
            "frontier_max": max_pq, "time_ms": round(elapsed, 2),
            "trace": exploration}


# ====================== IDA* ======================
# iterative deepening on f-cost threshold
# uses almost no memory (just the current path stack)
# but re-expands nodes across iterations

def run_ida_star(graph, orders, start, dest=None):
    t_start = time.perf_counter()
    s0 = init_state(start, orders)
    threshold = combined_h(s0, graph, orders, dest)

    # using lists so nested function can modify them
    expanded = [0]
    generated = [1]
    max_depth = [1]
    exploration = []
    path_stack = [s0]
    node_path = [s0[0]]

    FOUND = "FOUND"

    def search(g, bound):
        state = path_stack[-1]
        f = g + combined_h(state, graph, orders, dest)
        if f > bound:
            return f

        expanded[0] += 1
        exploration.append(state)

        if check_goal(state, dest):
            return FOUND

        min_cutoff = float('inf')
        for next_state, step_cost in successors(state, graph, orders):
            # cycle check on current path only (not global)
            if next_state in path_set:
                continue

            path_stack.append(next_state)
            path_set.add(next_state)
            node_path.append(next_state[0])
            generated[0] += 1
            if len(path_stack) > max_depth[0]:
                max_depth[0] = len(path_stack)

            result = search(g + step_cost, bound)

            if result == FOUND:
                return FOUND
            if result < min_cutoff:
                min_cutoff = result

            path_stack.pop()
            path_set.discard(next_state)
            node_path.pop()

        return min_cutoff

    # need higher recursion limit for K=6
    sys.setrecursionlimit(200000)

    path_set = {s0}
    iters = 0
    while True:
        iters += 1
        path_stack = [s0]
        path_set = {s0}
        node_path = [s0[0]]

        t = search(0, threshold)

        if t == FOUND:
            elapsed = (time.perf_counter() - t_start) * 1000
            cost = calc_path_cost(node_path, graph)
            # print(f"  IDA* finished in {iters} iterations")
            return {"algo": "IDA*", "path": list(node_path), "cost": cost,
                    "expanded": expanded[0], "generated": generated[0],
                    "frontier_max": max_depth[0],
                    "time_ms": round(elapsed, 2), "trace": exploration}

        if t == float('inf'):
            # no solution (shouldn't happen for connected graph)
            elapsed = (time.perf_counter() - t_start) * 1000
            return {"algo": "IDA*", "path": [], "cost": -1,
                    "expanded": expanded[0], "generated": generated[0],
                    "frontier_max": max_depth[0],
                    "time_ms": round(elapsed, 2), "trace": exploration}

        threshold = t
