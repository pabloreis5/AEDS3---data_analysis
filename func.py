import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Função para criar o grafo com os arquivos de entrada
def criar_grafo(politicians_file, graph_file):
    # Carregando os dados dos políticos
    politicians_data = pd.read_csv(politicians_file)
    
    # Criando um grafo direcionado
    G = nx.DiGraph()
    
    # Adicionando nós (deputados) ao grafo
    for _, row in politicians_data.iterrows():
        G.add_node(row['nome'], partido=row['partido'], votacoes=row['votacoes'])
    
    # Carregando os dados das votações em comum
    graph_data = pd.read_csv(graph_file)
    
    # Adicionando arestas ponderadas ao grafo
    for _, row in graph_data.iterrows():
        deputado1 = row['deputado1']
        deputado2 = row['deputado2']
        peso = row['votos_em_comum'] / min(G.nodes[deputado1]['votacoes'], G.nodes[deputado2]['votacoes'])
        G.add_edge(deputado1, deputado2, weight=peso)
    print("passou aq")
    
    return G

# Função para aplicar os filtros no grafo
def aplicar_filtros(grafo, ano=None, partidos=None):
    if ano:
        # Remove todas as arestas que não correspondem ao ano especificado
        arestas_a_remover = [(u, v) for u, v, d in grafo.edges(data=True) if d['ano'] != ano]
        grafo.remove_edges_from(arestas_a_remover)
    
    if partidos:
        # Remove todos os nós que não pertencem aos partidos especificados
        nos_a_remover = [n for n, d in grafo.nodes(data=True) if d['partido'] not in partidos]
        grafo.remove_nodes_from(nos_a_remover)

# Função para normalizar os pesos das arestas
def normalizar_pesos(grafo):
    for u, v, d in grafo.edges(data=True):
        grafo[u][v]['weight'] = d['weight'] / sum([grafo[x][v]['weight'] for x in grafo.predecessors(v)])

# Função para remover arestas com peso abaixo de um threshold
def remover_arestas_pouco_significativas(grafo, threshold):
    arestas_a_remover = [(u, v) for u, v, d in grafo.edges(data=True) if d['weight'] < threshold]
    grafo.remove_edges_from(arestas_a_remover)

# Função para inverter os pesos das arestas
def inverter_pesos(grafo):
    for u, v, d in grafo.edges(data=True):
        grafo[u][v]['weight'] = 1 - d['weight']

# Função para calcular a centralidade de betweenness
def calcular_centralidade_betweenness(grafo):
    centralidade = nx.betweenness_centrality(grafo, weight='weight')
    return centralidade

# Função para plotar o gráfico de barras da centralidade
def plotar_grafico_centralidade(centralidade):
    nomes = list(centralidade.keys())
    valores = list(centralidade.values())
    
    plt.figure(figsize=(12, 6))
    plt.bar(nomes, valores)
    plt.xlabel('Deputados')
    plt.ylabel('Centralidade de Betweenness')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()