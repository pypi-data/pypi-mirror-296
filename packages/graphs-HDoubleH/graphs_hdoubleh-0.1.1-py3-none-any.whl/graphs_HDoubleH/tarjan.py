class TarjanSCC:
    def __init__(self, graph):
        self.graph = graph
        self.V = len(graph)
        self.index = 0
        self.stack = []
        self.low = [-1] * self.V
        self.disc = [-1] * self.V
        self.in_stack = [False] * self.V
        self.sccs = []

    def _dfs(self, u):
        self.disc[u] = self.index
        self.low[u] = self.index
        self.index += 1
        self.stack.append(u)
        self.in_stack[u] = True

        # Consider all neighbors of u
        for v in self.graph.get(u, []):
            if self.disc[v] == -1:  # If v is not visited
                self._dfs(v)
                self.low[u] = min(self.low[u], self.low[v])
            elif self.in_stack[v]:  # If v is in the stack
                self.low[u] = min(self.low[u], self.disc[v])

        # If u is a root node, pop the stack to form an SCC
        if self.low[u] == self.disc[u]:
            scc = []
            while True:
                v = self.stack.pop()
                self.in_stack[v] = False
                scc.append(v)
                if v == u:
                    break
            self.sccs.append(scc)

    def find_sccs(self):
        for i in range(self.V):
            if self.disc[i] == -1:
                self._dfs(i)
        return self.sccs

# Example usage:
def tarjan_scc(graph):
    tarjan = TarjanSCC(graph)
    return tarjan.find_sccs()