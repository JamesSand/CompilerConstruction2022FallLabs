from backend.dataflow.basicblock import BasicBlock

"""
CFG: Control Flow Graph

nodes: sequence of basicblock
edges: sequence of edge(u,v), which represents after block u is executed, block v may be executed
links: links[u][0] represent the Prev of u, links[u][1] represent the Succ of u,
"""


class CFG:
    def __init__(self, nodes: list[BasicBlock], edges: list[(int, int)]) -> None:
        self.nodes = nodes
        self.edges = edges

        self.links = []

        for i in range(len(nodes)):
            self.links.append((set(), set()))

        for (u, v) in edges:
            self.links[u][1].add(v)
            self.links[v][0].add(u)

    def getBlock(self, id):
        return self.nodes[id]

    def getPrev(self, id):
        return self.links[id][0]

    def getSucc(self, id):
        return self.links[id][1]

    def getInDegree(self, id):
        return len(self.links[id][0])

    def getOutDegree(self, id):
        return len(self.links[id][1])

    def iterator(self):
        return iter(self.nodes)


    # my codes are below
    def unreachable(self, node) -> bool:
        # true for unreachable, false for reachable

        # serach for index
        id = self.nodes.index(node)
        
        # Implement dfs here
        stack = []
        stack.append(self.nodes[0])
        have_searched_list = []
        have_searched_list.append(0)

        while stack:
            current = stack.pop()
            nodes = self.getSucc(current)
            for i in nodes[::-1]: # since the last in stach, will be poped first, therefore need reverse here
                if i not in have_searched_list:
                    stack.append(i)
                    have_searched_list.append(i)

            if current == id:
                return False

        # unreachable! sad
        return True
