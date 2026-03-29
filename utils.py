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