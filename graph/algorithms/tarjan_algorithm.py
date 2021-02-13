from typing import Optional, Any

from graph.graph import *
from list.stack import *


class Tarjan:
    visited = 0
    dfs_num = 1
    low_link = 2
    found_scc = 3
    num = 0

    @classmethod
    def __find_strongly_connected(cls, vertex, stack, vertices) -> \
            Union[tuple[list["Vertex"], Optional[Any]], tuple[list["Vertex"], None]]:
        # print(vertex, vertices, stack)
        sub_solution = None
        sub_sub = None
        stack += vertex
        vertex_info = vertices.get(vertex)
        vertex_info[cls.dfs_num] = vertex_info[cls.low_link] = cls.num
        vertex_info[cls.visited] = True
        # print(vertex_info)
        cls.num += 1

        for edge in filter(lambda e: e.head.label != vertex.label, vertex.incidence):
            neighbour = edge.head
            # print(f"{vertex} -> {neighbour}")
            neighbour_info = vertices.get(neighbour)
            if not neighbour_info[cls.visited]:
                sub_solution, sub_sub = cls.__find_strongly_connected(neighbour, stack, vertices)
                vertex_info[cls.low_link] = min(neighbour_info[cls.low_link], vertex_info[cls.low_link])
                # print(vertex_info)
            else:
                vertex_info[cls.low_link] = min(neighbour_info[cls.dfs_num], vertex_info[cls.low_link])
                # print(vertex_info)

        # print(vertex, vertices, stack)
        if vertex_info[cls.low_link] == vertex_info[cls.dfs_num]:
            # print("here with, ", stack, vertex)
            scc_vertex = None
            scc_list = []
            while not scc_vertex == vertex:
                # print("3 is not None")
                scc_vertex = stack.pop()
                vertices.get(scc_vertex)[cls.visited] = False
                vertices.get(scc_vertex)[cls.found_scc] = True
                scc_list.append(scc_vertex)
            # print(f"returning: {scc_list} and {sub_solution}")
            return scc_list, sub_solution
        else:
            if sub_solution is not None:
                if sub_sub is not None:
                    sub_solution.append(sub_sub)
            return sub_solution, None

    @classmethod
    def tarjan(cls, g: "Graph") -> list[list["Vertex"]]:
        vertices = {key: [False, None, None, False] for key in g.vertices}
        n = len(vertices)
        stack = Stack(n)
        list_of_sccs = []
        for vertex in vertices:
            if not vertices.get(vertex)[cls.visited] and not vertices.get(vertex)[cls.found_scc]:
                scc, sub_scc = cls.__find_strongly_connected(vertex, stack, vertices)
                # print(scc, sub_scc, "final")
                if scc is not None:
                    # print("appending: ", scc)
                    list_of_sccs.append(scc)

                if sub_scc is not None:
                    # print("appending: ", sub_scc)
                    list_of_sccs.append(sub_scc)

        return list_of_sccs


if __name__ == '__main__':
    g = Graph(directed=True, n=3, cycle=True, cycle_length=3)
    v = Vertex(g)
    g.add_vertex(v)
    e = Edge(g.vertices[0], v)
    g.add_edge(e)
    f = Edge(g.vertices[2], v)
    g.add_edge(f)
    h = Edge(v, g.vertices[2])
    g.add_edge(h)

    print(g)
    print(Tarjan.tarjan(g))
