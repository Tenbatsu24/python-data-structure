from graph.graph import *
from list.stack import Stack


class HierHolzer:

    in_edge = 0
    out_edge = 1
    diff = 2

    def __init__(self, graph):
        self.graph = graph
        self.vertices = {}
        self.edge_count = self.get_in_and_out_edge()
        self.has_path, self.start_node = self.graph_has_eulerian_path()
        if self.start_node is None:
            # None is returned if there is no eulerian path
            # or there is an eulerian circuit in which case starting anywhere does not matter.
            self.start_node = graph.vertices[0]
        self.path = Stack(self.edge_count + 1)

    def euler_path(self):
        if not self.has_path:
            return None

        self.hier_holzer_dfs(self.start_node)

        if self.path.size != self.edge_count + 1:
            return None
        return Stack.to_array(self.path)

    def get_in_and_out_edge(self) -> int:
        directed = self.graph.directed
        edge_count = 0
        for vertex in self.graph.vertices:
            self.vertices[vertex] = [0, 0, 0]
            vertex_info = self.vertices[vertex]
            if not directed:
                vertex_info[self.in_edge] = vertex_info[self.out_edge] = vertex.degree
                edge_count += vertex.degree
            else:
                for edge in vertex.incidence:
                    if edge.head == vertex:
                        vertex_info[self.in_edge] += 1
                    if edge.tail == vertex:
                        vertex_info[self.out_edge] += 1
                    edge_count += 1
                vertex_info[self.diff] = vertex_info[self.out_edge] - vertex_info[self.in_edge]
        if directed:
            return edge_count
        else:
            return edge_count // 2

    def graph_has_eulerian_path(self):
        directed = self.graph.directed

        if self.edge_count == 0:
            return False, None

        start_node = None
        n_start_nodes = n_end_nodes = 0
        for vertex in self.vertices.keys():
            vertex_info = self.vertices[vertex]
            if -1 > vertex_info[self.diff] > 1:
                # check if number getting into node (getting out of node) more times than can get out (get in)
                # only one such instance is allowed, hence exclusive bounds. This is crucial only directed since
                # for undirected both in and out degree is same.
                return False, None
            elif vertex_info[self.in_edge] == vertex_info[self.out_edge] == 0:
                # check if disconnected. If disconnected then not possible to have euler path or circuit
                return False, None
            else:
                if directed:
                    # need to keep track of how many nodes exist such that in/out edge differ.
                    # in a directed directed graph the nodes with different in and out edges are the start/end nodes
                    # for an eulerian path.
                    # in an eulerian circuit all nodes would have same in and out degree.
                    if vertex_info[self.diff] == 1:
                        start_node = vertex
                        n_start_nodes += 1
                    elif vertex_info[self.diff] == -1:
                        n_end_nodes += 1
                else:
                    # if undirected we only need to compare in or out edge since they are both same
                    # if it has odd degree than only two such nodes are allowed else is fine, in the case of euler path
                    # in case of an eulerian circuit any all will hav even.
                    if vertex_info[self.out_edge] % 2 == 1:
                        start_node = vertex
                        n_start_nodes += 1
        if directed:
            # number of start and end nodes in a directed graph should both be exactly one or zero
            # else there is no eulerian path/circuit,
            # if there is path, return the start_node, in case of circuit this will be None
            return (n_start_nodes == 0 and n_end_nodes == 0) or (n_start_nodes == 1 and n_end_nodes == 1), start_node
        else:
            # in an undirected graph there can be two start, end nodes in case of an path
            # and in case of a circuit there can be 0 start_nodes since any is fine
            # return the start_node in case of a path, in case of circuit this will be None
            return (n_start_nodes == 0) or (n_start_nodes == 2), start_node

    def hier_holzer_dfs(self, vertex):
        vertex_info = self.vertices[vertex]
        while vertex_info[self.out_edge] != 0:
            neighbour = vertex.incidence[self.out_edge - 1].head
            vertex_info[self.out_edge] -= 1
            self.hier_holzer_dfs(neighbour)
        self.path += vertex


if __name__ == '__main__':
    g = Graph(directed=True, simple=False)
    for i in range(6):
        v = Vertex(g, i)
        g.add_vertex(v)
    v_s = g.vertices

    g.add_edge(Edge(v_s[0], v_s[1]))
    g.add_edge(Edge(v_s[0], v_s[2]))
    g.add_edge(Edge(v_s[1], v_s[1]))
    g.add_edge(Edge(v_s[1], v_s[3]))
    g.add_edge(Edge(v_s[2], v_s[0]))
    g.add_edge(Edge(v_s[2], v_s[1]))
    g.add_edge(Edge(v_s[2], v_s[4]))
    g.add_edge(Edge(v_s[3], v_s[1]))
    g.add_edge(Edge(v_s[3], v_s[2]))
    g.add_edge(Edge(v_s[3], v_s[5]))
    g.add_edge(Edge(v_s[4], v_s[5]))
    g.add_edge(Edge(v_s[5], v_s[2]))

    print(g)
    hier_holzer_solver = HierHolzer(g)
    print(hier_holzer_solver.euler_path())
    print(hier_holzer_solver.vertices)
    print(hier_holzer_solver.edge_count)
    print(hier_holzer_solver.path)
