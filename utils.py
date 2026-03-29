class State:
    def __init__(self, pos, pending_pickups, pending_deliveries):
        self.pos = pos
        self.pending_pickups = frozenset(pending_pickups)
        self.pending_deliveries = frozenset(pending_deliveries)

    def __hash__(self):
        return hash((self.pos, self.pending_pickups, self.pending_deliveries))

    def __eq__(self, other):
        return (self.pos == other.pos and
                self.pending_pickups == other.pending_pickups and
                self.pending_deliveries == other.pending_deliveries)

    def __repr__(self):
        return f"State(pos={self.pos}, pp={list(self.pending_pickups)}, pd={list(self.pending_deliveries)})"
    # problem class

from graph import GRAPH


class DeliveryProblem:
    def __init__(self, orders, start=12, goal=None):
        self.orders = orders
        self.start = start
        self.goal = goal if goal is not None else start

        # map index -> order
        self.order_map = {o.idx: o for o in orders}

    def initial_state(self):
        all_orders = [o.idx for o in self.orders]
        return State(self.start, all_orders, [])

    def is_goal(self, state):
        return (len(state.pending_pickups) == 0 and
                len(state.pending_deliveries) == 0 and
                state.pos == self.goal)

    def get_successors(self, state):
        successors = []

        for next_node, cost in GRAPH[state.pos]:

            new_pp = set(state.pending_pickups)
            new_pd = set(state.pending_deliveries)

            # check pickups
            for idx in list(new_pp):
                order = self.order_map[idx]
                if order.pickup == next_node:
                    new_pp.remove(idx)
                    new_pd.add(idx)

            # check deliveries
            for idx in list(new_pd):
                order = self.order_map[idx]
                if order.delivery == next_node:
                    new_pd.remove(idx)

            new_state = State(next_node, new_pp, new_pd)

            successors.append((new_state, cost))

        return successors