import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

def criar_grafo(ano, partidos=None):
    # Leitura do arquivo de políticos
    politicos_file = f'datasets/politicians{ano}.txt'
    politicos_df = pd.read_csv(politicos_file, sep='\t', header=None, names=['nome', 'partido', 'votacoes'])

    # Filtrar políticos por partido, se necessário
    if partidos:
        politicos_df = politicos_df[politicos_df['partido'].isin(partidos)]

    # Criação do grafo
    G = nx.Graph()

    # Leitura do arquivo de votações
    votacoes_file = f'datasets/graph{ano}.txt'
    votacoes_df = pd.read_csv(votacoes_file, sep='\t', header=None, names=['deputado1', 'deputado2', 'votacoes_iguais'])

    # Adicionar arestas ao grafo com peso igual ao número de votações iguais
    for _, row in votacoes_df.iterrows():
        deputado1 = row['deputado1']
        deputado2 = row['deputado2']
        votacoes_iguais = row['votacoes_iguais']
        G.add_edge(deputado1, deputado2, weight=votacoes_iguais, ano=ano)
        
    print("GRAFO CONSTRUIDO ### FILTRAGEM APLICADA")
    
    return G  # Retorna o grafo

# Função para criar e retornar um novo grafo normalizado a partir do grafo G
def criar_grafo_normalizado(grafo):
    # Cria uma cópia do grafo original para não modificá-lo
    grafo_normalizado = grafo.copy()
    
    # Lista de arestas a serem removidas
    arestas_remover = []
    
    # Normalizar os pesos das arestas do grafo normalizado
    for u, v, w in grafo_normalizado.edges(data=True):
        # Obter o número mínimo de votações entre os deputados u e v
        min_votes = min(w['weight'], grafo_normalizado[v][u]['weight'])  # Ajustado para considerar ambas as direções
        
        # Normalizar o peso da aresta com base na fórmula fornecida
        if min_votes > 0:
            grafo_normalizado[u][v]['weight'] = w['weight'] / min_votes
        else:
            # Marcar a aresta para remoção se não houver votações em comum
            arestas_remover.append((u, v))
    
    # Remover arestas marcadas para remoção
    for u, v in arestas_remover:
        grafo_normalizado.remove_edge(u, v)
    
    print("GRAFO NORMALIZADO ###")
    return grafo_normalizado