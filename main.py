from func import *
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

# Pablo Batista de Andrade Reis - 20.1.8106
# Laura Chaves Soares - 21.1.8125

ano = 2023
partidos_filtrados = ["PT", "PSOL"]
threshold = 0.9

G_sem_filtro = criar_grafo(ano)
G_filtrado = filtrar_grafo_por_partidos(G_sem_filtro, ano, partidos_filtrados)
grafo_normalizado = criar_grafo_normalizado(G_filtrado)
grafo_threshold = criar_grafo_threshold(grafo_normalizado, threshold)
inverter_pesos(grafo_threshold)


# Calcular a Betweenness Centrality
betweenness_centrality = nx.betweenness_centrality(grafo_threshold)

# Converter o dicionário de centralidades em listas separadas para o gráfico
nomes_deputados = list(betweenness_centrality.keys())
centralidade_valores = list(betweenness_centrality.values())

# Criar o gráfico de barras
plt.figure(figsize=(12, 6))
plt.barh(nomes_deputados, centralidade_valores, color='skyblue')
plt.xlabel('Medida de Centralidade')
plt.ylabel('Deputados')
plt.title('Betweenness Centrality dos Deputados')

# Salvar o gráfico em um arquivo de imagem (opcional)
plt.savefig('betweenness_centrality.png')

# Exibir o gráfico
plt.show()

#--------------------------------------

# Calcular a matriz de adjacência do grafo normalizado
adj_matrix = nx.to_pandas_adjacency(grafo_normalizado).values

# Converter a matriz de adjacência em um DataFrame do pandas
df = pd.DataFrame(adj_matrix, columns=grafo_normalizado.nodes(), index=grafo_normalizado.nodes())

# Criar um mapa de calor usando seaborn
plt.figure(figsize=(12, 10))
sns.heatmap(df, cmap='coolwarm', annot=True, fmt=".1f", cbar=False)
plt.title('Mapa de Calor - Correlação entre Deputados')
plt.xlabel('Deputados')
plt.ylabel('Deputados')

# Salvar o mapa de calor em um arquivo de imagem (opcional)
plt.savefig('heatmap.png')

# Exibir o mapa de calor
plt.show()


#-------------------------------------
# Criar um layout de mola para o grafo_threshold
layout = nx.spring_layout(grafo_threshold, seed=42)  # O 'seed' é opcional para reproduzibilidade

# Plotar o grafo_threshold
plt.figure(figsize=(12, 10))
nx.draw(grafo_threshold, pos=layout, with_labels=True, node_size=50, node_color='skyblue', font_size=8, font_color='black', font_weight='bold', edge_color='gray', width=0.5)

# Definir títulos e rótulos
plt.title('Grafo de Relações de Votos Entre Deputados (com Threshold)')
plt.xlabel('Deputados')
plt.ylabel('Deputados')

# Salvar o gráfico em um arquivo de imagem (por exemplo, formato PNG)
plt.savefig('grafo_threshold.png')

# Exibir o grafo_threshold
plt.show()