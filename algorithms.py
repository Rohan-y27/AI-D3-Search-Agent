def dfs(problem):
    start = problem.initial_state()

    stack = []
    stack.append((start, [start.pos], 0))  # (state, path, cost)

    visited = set()

    nodes_expanded = 0

    while stack:
        state, path, cost = stack.pop()
        nodes_expanded += 1

        if state in visited:
            continue

        visited.add(state)

        if problem.is_goal(state):
            return {
                "algorithm": "DFS",
                "path": path,
                "cost": cost,
                "expanded": nodes_expanded
            }

        for next_state, edge_cost in problem.get_successors(state):
            stack.append((
                next_state,
                path + [next_state.pos],
                cost + edge_cost
            ))

    return {
        "algorithm": "DFS",
        "path": None,
        "cost": None,
        "expanded": nodes_expanded
    }

#starting BFS
from collections import deque


def bfs(problem):
    start = problem.initial_state()

    queue = deque()
    queue.append((start, [start.pos], 0))  # (state, path, cost)

    visited = set()
    visited.add(start)

    nodes_expanded = 0

    while queue:
        state, path, cost = queue.popleft()
        nodes_expanded += 1

        if problem.is_goal(state):
            return {
                "algorithm": "BFS",
                "path": path,
                "cost": cost,
                "expanded": nodes_expanded
            }

        for next_state, edge_cost in problem.get_successors(state):
            if next_state not in visited:
                visited.add(next_state)
                queue.append((
                    next_state,
                    path + [next_state.pos],
                    cost + edge_cost
                ))

    return {
        "algorithm": "BFS",
        "path": None,
        "cost": None,
        "expanded": nodes_expanded
    }
#starting A*
import heapq


def astar(problem):
    start = problem.initial_state()

    # (cost, state, path)
    heap = []
    heapq.heappush(heap, (0, start, [start.pos]))

    visited = {}

    nodes_expanded = 0

    while heap:
        g, state, path = heapq.heappop(heap)
        nodes_expanded += 1

        # skip if already visited with lower cost
        if state in visited and visited[state] <= g:
            continue

        visited[state] = g

        if problem.is_goal(state):
            return {
                "algorithm": "A*",
                "path": path,
                "cost": g,
                "expanded": nodes_expanded
            }

        for next_state, edge_cost in problem.get_successors(state):
            new_cost = g + edge_cost

            heapq.heappush(heap, (
                new_cost,
                next_state,
                path + [next_state.pos]
            ))

    return {
        "algorithm": "A*",
        "path": None,
        "cost": None,
        "expanded": nodes_expanded
    }