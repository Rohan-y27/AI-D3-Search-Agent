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