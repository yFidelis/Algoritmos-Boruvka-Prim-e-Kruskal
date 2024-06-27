import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from tkinter import filedialog
import time


class GraphGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Graph Editor")

        self.graph = nx.Graph()

        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(111)
        self.canvas_ntk = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas_ntk.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.add_label = tk.Label(master, text="Vértice:")
        self.add_label.pack()
        self.add_entry = tk.Entry(master)
        self.add_entry.pack()
        self.add_button = tk.Button(master, text="Adicionar Vértice", command=self.add_vertex)
        self.add_button.pack()

        self.remove_label = tk.Label(master, text="Vértice a Remover:")
        self.remove_label.pack()
        self.remove_entry = tk.Entry(master)
        self.remove_entry.pack()
        self.remove_button = tk.Button(master, text="Remover Vértice", command=self.remove_vertex)
        self.remove_button.pack()

        self.edge_label = tk.Label(master, text="Aresta (Origem-Destino):")
        self.edge_label.pack()
        self.edge_origin_entry = tk.Entry(master)
        self.edge_origin_entry.pack()
        self.edge_dest_entry = tk.Entry(master)
        self.edge_dest_entry.pack()
        self.edge_weight_label = tk.Label(master, text="Peso:")
        self.edge_weight_label.pack()
        self.edge_weight_entry = tk.Entry(master)
        self.edge_weight_entry.pack()
        self.edge_button = tk.Button(master, text="Adicionar Aresta", command=self.add_edge)
        self.edge_button.pack()

        self.load_button = tk.Button(master, text="Carregar Grafo", command=self.load_graph)
        self.load_button.pack()

        self.save_button = tk.Button(master, text="Salvar Grafo", command=self.save_graph)
        self.save_button.pack()

        self.prim_button = tk.Button(master, text="Prim", command=self.calculate_prim)
        self.prim_button.pack()

        self.boruvka_button = tk.Button(master, text="Borůvka", command=self.calculate_boruvka)
        self.boruvka_button.pack()

        self.kruskal_button = tk.Button(master, text="Kruskal", command=self.calculate_kruskal)
        self.kruskal_button.pack()



        self.draw_graph()

    def add_vertex(self):
        vertex = self.add_entry.get()
        if vertex:
            self.graph.add_node(vertex)
            self.draw_graph()
            self.add_entry.delete(0, tk.END)

    def remove_vertex(self):
        vertex = self.remove_entry.get()
        if vertex:
            if vertex in self.graph.nodes():
                self.graph.remove_node(vertex)
                self.draw_graph()
            else:
                print("Vértice não encontrado.")
            self.remove_entry.delete(0, tk.END)

    def add_edge(self):
        origin = self.edge_origin_entry.get()
        dest = self.edge_dest_entry.get()
        weight = self.edge_weight_entry.get()
        if origin and dest and weight:
            self.graph.add_edge(origin, dest, weight=float(weight))
            self.draw_graph()
            self.edge_origin_entry.delete(0, tk.END)
            self.edge_dest_entry.delete(0, tk.END)
            self.edge_weight_entry.delete(0, tk.END)

    def load_graph(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename:
            df = pd.read_csv(filename)
            self.graph = nx.from_pandas_edgelist(df, 'Origem', 'Destino', ['Peso'])
            for u, v, data in self.graph.edges(data=True):
                data['weight'] = float(data['Peso'])
            self.draw_graph()

    def save_graph(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            edges = self.graph.edges(data=True)
            df = pd.DataFrame([(u, v, d['weight']) for u, v, d in edges], columns=['Origem', 'Destino', 'Peso'])
            df.to_csv(filename, index=False)

    def draw_graph(self):
        self.ax.clear()
        pos = nx.planar_layout(self.graph)
        nx.draw(self.graph, pos, ax=self.ax, with_labels=True, node_size=500, node_color='skyblue')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=nx.get_edge_attributes(self.graph, 'weight'))
        self.canvas_ntk.draw()


    def calculate_prim(self):
        if not self.graph.nodes:
            print("Grafo vazio.")
            return
        
        mst = nx.Graph()
        mst.add_nodes_from(self.graph.nodes(data=True))
        visited = set()
        edges = list(self.graph.edges(data=True))
        pos = nx.planar_layout(self.graph)
        
        start_node = next(iter(self.graph.nodes))
        visited.add(start_node)
        
        while len(visited) < len(self.graph.nodes):
            edge = min((e for e in edges if (e[0] in visited and e[1] not in visited) or 
                                        (e[1] in visited and e[0] not in visited)),
                    key=lambda x: x[2]['weight'])
            
            edges.remove(edge)
            if edge[0] in visited:
                mst.add_edge(edge[0], edge[1], weight=edge[2]['weight'])
                visited.add(edge[1])
            else:
                mst.add_edge(edge[1], edge[0], weight=edge[2]['weight'])
                visited.add(edge[0])
            
            self.ax.clear()
            node_colors = ['red' if n in visited else 'skyblue' for n in self.graph.nodes]
            edge_colors = ['red' if (u, v) in mst.edges or (v, u) in mst.edges else 'black' for u, v in self.graph.edges]
            nx.draw(self.graph, pos, ax=self.ax, with_labels=True, node_size=500, node_color=node_colors, edge_color=edge_colors)
            nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=nx.get_edge_attributes(self.graph, 'weight'))
            self.canvas_ntk.draw()
            self.master.update_idletasks()
            time.sleep(1)
        
        self.ax.clear()
        nx.draw(mst, pos, ax=self.ax, with_labels=True, node_size=500, node_color='lightgreen')
        nx.draw_networkx_edge_labels(mst, pos, edge_labels=nx.get_edge_attributes(mst, 'weight'))
        self.canvas_ntk.draw()

    def calculate_boruvka(self):
        def find_component(node, parent):
            if parent[node] == node:
                return node
            else:
                parent[node] = find_component(parent[node], parent)
                return parent[node]

        def union_components(u, v, parent, rank):
            root_u = find_component(u, parent)
            root_v = find_component(v, parent)
            if root_u != root_v:
                if rank[root_u] > rank[root_v]:
                    parent[root_v] = root_u
                elif rank[root_u] < rank[root_v]:
                    parent[root_u] = root_v
                else:
                    parent[root_v] = root_u
                    rank[root_u] += 1

        if not self.graph.edges:
            print("Grafo vazio.")
            return

        parent = {node: node for node in self.graph.nodes()}
        rank = {node: 0 for node in self.graph.nodes()}
        mst = nx.Graph()
        mst.add_nodes_from(self.graph.nodes(data=True))
        pos = nx.planar_layout(self.graph)

        num_components = len(self.graph.nodes)
        while num_components > 1:
            cheapest_edges = {}
            for u, v, data in self.graph.edges(data=True):
                component_u = find_component(u, parent)
                component_v = find_component(v, parent)
                if component_u != component_v:
                    if component_u not in cheapest_edges or cheapest_edges[component_u][2]['weight'] > data['weight']:
                        cheapest_edges[component_u] = (u, v, data)
                    if component_v not in cheapest_edges or cheapest_edges[component_v][2]['weight'] > data['weight']:
                        cheapest_edges[component_v] = (u, v, data)

            for u, v, data in cheapest_edges.values():
                component_u = find_component(u, parent)
                component_v = find_component(v, parent)
                if component_u != component_v:
                    mst.add_edge(u, v, weight=data['weight'])
                    union_components(u, v, parent, rank)
                    num_components -= 1

            self.ax.clear()
            components = list(nx.connected_components(mst))
            colors = ['red', 'blue', 'green', 'purple', 'orange', 'yellow']
            color_map = {}
            for idx, component in enumerate(components):
                for node in component:
                    color_map[node] = colors[idx % len(colors)]
            node_colors = [color_map[node] for node in mst.nodes()]
            edge_colors = ['red' if (u, v) in mst.edges or (v, u) in mst.edges else 'black' for u, v in self.graph.edges]
            nx.draw(self.graph, pos, ax=self.ax, with_labels=True, node_size=500, node_color=node_colors, edge_color=edge_colors)
            nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=nx.get_edge_attributes(self.graph, 'weight'))
            self.canvas_ntk.draw()
            self.master.update_idletasks()
            time.sleep(5)

        self.ax.clear()
        components = list(nx.connected_components(mst))
        color_map = {}
        for idx, component in enumerate(components):
            for node in component:
                color_map[node] = colors[idx % len(colors)]
        node_colors = [color_map[node] for node in mst.nodes()]
        nx.draw(mst, pos, ax=self.ax, with_labels=True, node_size=500, node_color=node_colors)
        nx.draw_networkx_edge_labels(mst, pos, edge_labels=nx.get_edge_attributes(mst, 'weight'))
        self.canvas_ntk.draw()
    
    def calculate_kruskal(self):
        mst = self.kruskal_algorithm()
        self.ax.clear()
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, ax=self.ax, with_labels=True, node_size=500, node_color='skyblue')
        nx.draw_networkx_edges(self.graph, pos, edgelist=mst, edge_color='red', width=2)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=nx.get_edge_attributes(self.graph, 'weight'))
        self.canvas_ntk.draw()

    def kruskal_algorithm(self):
        mst = []
        edges = list(self.graph.edges(data=True))
        edges.sort(key=lambda x: x[2]['weight'])

        parent = {node: node for node in self.graph.nodes()}
        rank = {node: 0 for node in self.graph.nodes()}

        def find(node):
            if parent[node] != node:
                parent[node] = find(parent[node])
            return parent[node]

        def union(node1, node2):
            root1 = find(node1)
            root2 = find(node2)
            if root1 != root2:
                if rank[root1] > rank[root2]:
                    parent[root2] = root1
                elif rank[root1] < rank[root2]:
                    parent[root1] = root2
                else:
                    parent[root2] = root1
                    rank[root1] += 1

        for edge in edges:
            node1, node2, weight = edge
            if find(node1) != find(node2):
                union(node1, node2)
                mst.append((node1, node2))

        return mst

def main():
    root = tk.Tk()
    app = GraphGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
