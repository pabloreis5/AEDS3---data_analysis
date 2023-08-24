from func import *
import networkx as nx
import matplotlib.pyplot as plt


ano = 2022
partidos = ["PT", "PL", "MDB"]
threshold = 0.5

G = criar_grafo(ano, partidos)
grafo_normalizado = criar_grafo_normalizado(G)
grafo_threshold = criar_grafo_threshold(grafo_normalizado, threshold)



# Crie um layout para o grafo para posicionar os nós
layout = nx.spring_layout(grafo_threshold)

# Extraia os pesos das arestas para determinar a espessura das arestas no gráfico
edge_weights = [grafo_threshold[u][v]['weight'] for u, v in grafo_threshold.edges()]

# Crie o plot do grafo
plt.figure(figsize=(10, 10))  # Ajuste o tamanho da figura conforme necessário
nx.draw(grafo_threshold, pos=layout, with_labels=True, node_size=50, font_size=8, width=edge_weights, edge_cmap=plt.cm.Blues)

# Exiba o gráfico
plt.show()