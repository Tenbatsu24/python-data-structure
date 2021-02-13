import math

from heap.heap import Heap
from graph.graph import *


def edge_relaxed(edge: "Edge", directed: bool, start_v: "Vertex", min_heap: Heap = None) -> bool:
    # print(edge)
    relaxed = relax_edge(edge, edge.tail, edge.head, edge.weight, start_v, min_heap)
    if not directed:
        relaxed = relaxed or relax_edge(edge, edge.head, edge.tail, edge.weight, start_v, min_heap)
    return relaxed


def relax_edge(edge, u, v, weight, start_v, min_heap: "Heap" = None):
    if v.label != start_v.label and u.dist + weight < v.dist:
        v.dist = u.dist + weight
        v.in_edge = edge
        if min_heap is not None:
            # print(f"I decr key: {edge.head.__repr__()}")
            min_heap.decr_key(v)
        return True
    return False


def bellman_ford_undirected(graph: "Graph", start):
    """
    Arguments: <graph> is a graph object, where edges have integer <weight>
        attributes,	and <start> is a vertex of <graph>.
    Action: Uses the Bellman-Ford algorithm to compute all vertex distances
        from <start> in <graph>, and assigns these values to the vertex attribute <dist>.
        Optional: assigns the vertex attribute <in_edge> to be the incoming
        shortest path edge, for every reachable vertex except <start>.
        <graph> is viewed as an undirected graph.
    """
    # Initialize the vertex attributes:
    init_search(graph, start)

    iterations = len(graph.vertices) - 1
    i = 0
    changed = True
    while i < iterations and changed:
        changed = False
        for e in graph.edges:
            if edge_relaxed(e, False, start):
                changed = True
        i += 1

    for edge in graph.edges:
        if edge.head.dist > edge.tail.dist + edge.weight:
            show_warning_bellman(edge)


def show_warning_bellman(edge):
    print('\033[93m' + "Negative Cycle Detected- > "
                       f"Triangle Inequality violated after n-1 iterations on edge: " +
          f"{edge.tail}->{edge.head}:{edge.weight} and dist(u)={edge.tail.dist}, " +
          f"dist(v):{edge.head.dist}" + '\033[0m'
          )


def bellman_ford_directed(graph, start):
    init_search(graph, start)

    iterations = len(graph.vertices) - 1
    i = 0
    changed = True
    while i < iterations and changed:
        changed = False
        for e in graph.edges:
            if edge_relaxed(e, True, start):
                changed = True
        i += 1

    for e in graph.edges:
        if e.tail.dist + e.weight < e.head.dist:
            show_warning_bellman(e)


def find_min(vertices: list["Vertex"]) -> "Vertex":
    v_to_return = vertices[0]
    min_dist = v_to_return.dist
    for candidate in vertices[1:]:
        if candidate.dist < min_dist:
            v_to_return = candidate
            min_dist = candidate.dist
    return v_to_return


def show_warning_dijkstra(edge):
    print(
        '\033[93m' +
        f"The given graph contains a negative edge:{edge,}, dijkstra will not provide a proper answer." +
        '\033[0m')


def dijkstra_undirected(graph: "Graph", start: "Vertex"):
    """
    Arguments: <graph> is a graph object, where edges have integer <weight>
        attributes,	and <start> is a vertex of <graph>.
    Action: Uses Dijkstra's algorithm to compute all vertex distances
        from <start> in <graph>, and assigns these values to the vertex attribute <dist>.
        Optional: assigns the vertex attribute <in_edge> to be the incoming
        shortest path edge, for every reachable vertex except <start>.
        <graph> is viewed as an undirected graph.
    """
    # Initialize the vertex attributes:
    init_search(graph, start)
    min_heap = Heap(len(graph.vertices))

    for vertica in graph.vertices:
        min_heap += vertica

    while min_heap:
        # print(min_heap.count)
        v = min_heap.pop()
        for edge in v.incidence:
            if edge.weight < 0:
                show_warning_dijkstra(edge)
            edge_relaxed(edge, False, start, min_heap)


def dijkstra_directed(graph, start):
    """
    Arguments: <graph> is a graph object, where edges have integer <weight>
        attributes,	and <start> is a vertex of <graph>.
    Action: Uses Dijkstra's algorithm to compute all vertex distances
        from <start> in <graph>, and assigns these values to the vertex attribute <dist>.
        Optional: assigns the vertex attribute <in_edge> to be the incoming
        shortest path edge, for every reachable vertex except <start>.
        <graph> is viewed as a directed graph.
    """
    # Initialize the vertex attributes:
    init_search(graph, start)
    min_heap = Heap(len(graph.vertices))

    for vertica in graph.vertices:
        min_heap += vertica

    # print(min_heap, len(min_heap))
    while min_heap:
        v = min_heap.pop()
        # print(f"Just popped: {v, v.dist}")
        # print(len(min_heap), min_heap)
        for edge in filter(lambda e: e.tail == v, v.incidence):
            if edge.weight < 0:
                show_warning_dijkstra(edge)
            # print(f"Before:{edge, edge.tail.dist, edge.head.dist, edge.weight}")
            edge_relaxed(edge, True, start, min_heap)
            # print(f"After: {edge, edge.tail.dist, edge.head.dist, edge.weight}")


def init_search(graph: "Graph", start: "Vertex"):
    for v in graph.vertices:
        v.dist = math.inf
        v.in_edge = None
    start.dist = 0
