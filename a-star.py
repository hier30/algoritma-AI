import heapq
import networkx as nx
import matplotlib.pyplot as plt

# Data graf dan heuristik sama seperti sebelumnya
romania_map = {
    'Arad': [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)],
    'Zerind': [('Oradea', 71), ('Arad', 75)],
    'Oradea': [('Sibiu', 151), ('Zerind', 71)],
    'Sibiu': [('Fagaras', 99), ('Rimnicu Vilcea', 80), ('Oradea', 151), ('Arad', 140)],
    'Timisoara': [('Lugoj', 111), ('Arad', 118)],
    'Lugoj': [('Mehadia', 70), ('Timisoara', 111)],
    'Mehadia': [('Drobeta', 75), ('Lugoj', 70)],
    'Drobeta': [('Craiova', 120), ('Mehadia', 75)],
    'Craiova': [('Pitesti', 138), ('Rimnicu Vilcea', 146), ('Drobeta', 120)],
    'Rimnicu Vilcea': [('Pitesti', 97), ('Sibiu', 80), ('Craiova', 146)],
    'Fagaras': [('Bucharest', 211), ('Sibiu', 99)],
    'Pitesti': [('Bucharest', 101), ('Rimnicu Vilcea', 97), ('Craiova', 138)],
    'Bucharest': [('Fagaras', 211), ('Pitesti', 101)],
}

heuristic = {
    'Arad': 366, 'Zerind': 374, 'Oradea': 380, 'Sibiu': 253,
    'Timisoara': 329, 'Lugoj': 244, 'Mehadia': 241, 'Drobeta': 242,
    'Craiova': 160, 'Rimnicu Vilcea': 193, 'Fagaras': 176,
    'Pitesti': 100, 'Bucharest': 0
}

# A* Search Algorithm
def a_star_search(start, goal):
    open_set = []
    heapq.heappush(open_set, (heuristic[start], 0, start, [start]))
    visited = set()

    while open_set:
        _, cost_so_far, current, path = heapq.heappop(open_set)

        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            return path, cost_so_far

        for neighbor, step_cost in romania_map.get(current, []):
            if neighbor not in visited:
                new_cost = cost_so_far + step_cost
                est_cost = new_cost + heuristic[neighbor]
                heapq.heappush(open_set, (est_cost, new_cost, neighbor, path + [neighbor]))
    return None, float('inf')

# Visualisasi
def visualize_path(graph, path):
    G = nx.Graph()

    for city, neighbors in graph.items():
        for neighbor, distance in neighbors:
            G.add_edge(city, neighbor, weight=distance)

    pos = nx.spring_layout(G, seed=42)  # tata letak graf

    # Gambar semua node dan edge
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True, node_size=800, node_color='lightblue')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Highlight jalur hasil A*
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='salmon')

    plt.title("Visualisasi A* Path dari {} ke {}".format(path[0], path[-1]))
    plt.show()

# Contoh penggunaan
start = 'Arad'
goal = 'Bucharest'
path, cost = a_star_search(start, goal)

print("Rute terbaik:", " -> ".join(path))
print("Total jarak:", cost, "km")

visualize_path(romania_map, path)
