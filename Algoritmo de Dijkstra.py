##________  ___  ___  ________  ___      ___ ________     
##|\   ____\|\  \|\  \|\   __  \|\  \    /  /|\   __  \    
##\ \  \___|\ \  \\\  \ \  \|\  \ \  \  /  / | \  \|\  \   
## \ \  \    \ \   __  \ \   __  \ \  \/  / / \ \   __  \  
##  \ \  \____\ \  \ \  \ \  \ \  \ \    / /   \ \  \ \  \ 
##   \ \_______\ \__\ \__\ \__\ \__\ \__/ /     \ \__\ \__\
##    \|_______|\|__|\|__|\|__|\|__|\|__|/       \|__|\|__|
##21310195 Meza Morales Salvador Emmanuel
import tkinter as tk
from tkinter import ttk, messagebox
import heapq
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.edges = {}
        self.vertices = set()

    def add_edge(self, u, v, weight):
        if u not in self.edges:
            self.edges[u] = []
        if v not in self.edges:
            self.edges[v] = []
        self.edges[u].append((weight, v))
        self.edges[v].append((weight, u))
        self.vertices.add(u)
        self.vertices.add(v)

    def dijkstra(self, start):
        min_heap = [(0, start)]
        distances = {v: float('inf') for v in self.vertices}
        distances[start] = 0
        previous = {v: None for v in self.vertices}
        steps = []
        while min_heap:
            current_distance, current_vertex = heapq.heappop(min_heap)
            if current_distance > distances[current_vertex]:
                continue
            steps.append((current_vertex, list(distances.items()), previous.copy()))
            for weight, neighbor in self.edges[current_vertex]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_vertex
                    heapq.heappush(min_heap, (distance, neighbor))
        return distances, previous, steps

class DijkstraApp:
    def __init__(self, root):
        self.root = root
        self.graph = Graph()
        self.create_widgets()

    def create_widgets(self):
        self.root.title("Algoritmo de Dijkstra - AEM")
        self.root.geometry("600x500")

        self.edge_frame = ttk.Frame(self.root)
        self.edge_frame.pack(pady=5)

        self.u_label = ttk.Label(self.edge_frame, text="Vértice U:")
        self.u_label.grid(row=0, column=0, padx=5, pady=5)
        self.u_entry = ttk.Entry(self.edge_frame)
        self.u_entry.grid(row=0, column=1, padx=5, pady=5)

        self.v_label = ttk.Label(self.edge_frame, text="Vértice V:")
        self.v_label.grid(row=1, column=0, padx=5, pady=5)
        self.v_entry = ttk.Entry(self.edge_frame)
        self.v_entry.grid(row=1, column=1, padx=5, pady=5)

        self.weight_label = ttk.Label(self.edge_frame, text="Peso:")
        self.weight_label.grid(row=2, column=0, padx=5, pady=5)
        self.weight_entry = ttk.Entry(self.edge_frame)
        self.weight_entry.grid(row=2, column=1, padx=5, pady=5)

        self.add_edge_button = ttk.Button(self.edge_frame, text="Agregar Arista", command=self.add_edge)
        self.add_edge_button.grid(row=3, column=0, columnspan=2, pady=5)

        self.show_edges_button = ttk.Button(self.root, text="Mostrar Aristas Guardadas", command=self.show_edges)
        self.show_edges_button.pack(pady=5)

        self.start_label = ttk.Label(self.root, text="Seleccione el vértice inicial:")
        self.start_label.pack(pady=5)
        self.start_entry = ttk.Entry(self.root)
        self.start_entry.pack(pady=5)

        self.solve_button = ttk.Button(self.root, text="Resolver", command=self.solve)
        self.solve_button.pack(pady=5)

        self.result_text = tk.Text(self.root, height=10)
        self.result_text.pack(pady=5)

    def add_edge(self):
        u = self.u_entry.get()
        v = self.v_entry.get()
        try:
            weight = int(self.weight_entry.get())
        except ValueError:
            messagebox.showerror("Error", "El peso debe ser un número entero.")
            return
        self.graph.add_edge(u, v, weight)
        messagebox.showinfo("Información", f"Arista {u}-{v} con peso {weight} agregada.")

    def show_edges(self):
        edges_text = "Aristas guardadas:\n"
        for u in self.graph.edges:
            for weight, v in self.graph.edges[u]:
                edges_text += f"{u} - {v} con peso {weight}\n"
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, edges_text)

    def solve(self):
        start = self.start_entry.get()
        if start not in self.graph.vertices:
            messagebox.showerror("Error", "El vértice inicial no existe en el grafo.")
            return
        
        distances, previous, steps = self.graph.dijkstra(start)
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Distancias mínimas desde el vértice inicial:\n")
        for v, distance in distances.items():
            self.result_text.insert(tk.END, f"{v}: {distance}\n")

        self.show_graph(initial=True)
        self.show_steps(steps)

    def show_graph(self, initial=True):
        G = nx.Graph()
        for u in self.graph.edges:
            for weight, v in self.graph.edges[u]:
                G.add_edge(u, v, weight=weight)

        pos = nx.spring_layout(G)
        plt.figure(figsize=(10, 7))
        if initial:
            title = "Grafo Inicial"
            nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
            labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        else:
            title = "Distancias Mínimas"
            nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
            labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
            for u, v in G.edges():
                plt.text((pos[u][0] + pos[v][0]) / 2, (pos[u][1] + pos[v][1]) / 2, str(G[u][v]['weight']), fontsize=10, color='red')
        plt.title(title)
        plt.show()

    def show_steps(self, steps):
        G = nx.Graph()
        for u in self.graph.edges:
            for weight, v in self.graph.edges[u]:
                G.add_edge(u, v, weight=weight)

        pos = nx.spring_layout(G)

        for i, (current_vertex, distances, previous) in enumerate(steps):
            plt.figure(figsize=(10, 7))
            nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
            labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
            nx.draw_networkx_nodes(G, pos, nodelist=[current_vertex], node_color='green', node_size=700)
            plt.title(f"Paso {i + 1} - Vértice Actual: {current_vertex}")
            plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = DijkstraApp(root)
    root.mainloop()

