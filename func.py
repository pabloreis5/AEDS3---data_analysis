import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

def criar_grafo(ano):
    # Leitura do arquivo de votações com delimitador ponto e vírgula
    votacoes_file = f'datasets/graph{ano}.txt'
    votacoes_df = pd.read_csv(votacoes_file, sep=';', header=None, names=['deputado1', 'deputado2', 'votacoes_iguais'])

    # Criação do grafo
    G = nx.Graph()

    # Adicionar arestas ao grafo com peso igual ao número de votações iguais
    for _, row in votacoes_df.iterrows():
        deputado1 = row['deputado1']
        deputado2 = row['deputado2']
        votacoes_iguais = row['votacoes_iguais']
        G.add_edge(deputado1, deputado2, weight=votacoes_iguais, ano=ano)

    print(f"GRAFO CONSTRUIDO: Nós={len(G.nodes())}, Arestas={len(G.edges())}")

    return G  # Retorna o grafo

def filtrar_grafo_por_partidos(grafo, ano, partidos=None):
    if partidos is None:
        # Se nenhum partido for especificado, retornar o grafo original sem filtro
        return grafo

    # Leitura do arquivo de políticos
    politicos_file = f'datasets/politicians{ano}.txt'
    politicos_df = pd.read_csv(politicos_file, sep=';', header=None, names=['nome', 'partido', 'votacoes'])

    # Filtrar políticos por partido
    politicos_filtrados = politicos_df[politicos_df['partido'].isin(partidos)]
    deputados_filtrados = politicos_filtrados['nome'].tolist()

    # Criar um novo grafo filtrado com base nos deputados do partido
    G_filtrado = grafo.subgraph(deputados_filtrados).copy()

    print(f"GRAFO FILTRADO POR PARTIDOS ({', '.join(partidos)}): Nós={len(G_filtrado.nodes())}, Arestas={len(G_filtrado.edges())}")

    return G_filtrado


# Função para criar e retornar um novo grafo normalizado a partir do grafo G
def criar_grafo_normalizado(grafo):
    # Cria uma cópia do grafo original para não modificá-lo
    grafo_normalizado = grafo.copy()
    
    # Iterar sobre as arestas do grafo normalizado
    for u, v, w in grafo_normalizado.edges(data=True):
        # Normalizar o peso da aresta com base na fórmula fornecida
        grafo_normalizado[u][v]['weight'] = w['weight'] / min(grafo.degree(u), grafo.degree(v))
            
    # Imprimir o número de nós e arestas no grafo normalizado
    num_nos = len(grafo_normalizado.nodes())
    num_arestas = len(grafo_normalizado.edges())
    print(f"GRAFO NORMALIZADO ### Nós={num_nos}, Arestas={num_arestas}")
    
    return grafo_normalizado



def criar_grafo_threshold(grafo_normalizado, threshold):
    # Cria uma cópia do grafo normalizado original para não modificá-lo
    grafo_com_threshold = grafo_normalizado.copy()
    
    # Lista de arestas a serem removidas
    arestas_remover = []
    
    
    # Itera sobre as arestas do grafo normalizado com threshold
    for u, v, w in grafo_com_threshold.edges(data=True):
        if w['weight'] < threshold:
            # Marcar a aresta para remoção se o peso for menor que o threshold
            arestas_remover.append((u, v))
    
    # Remover arestas marcadas para remoção
    for u, v in arestas_remover:
        grafo_com_threshold.remove_edge(u, v)
        
    # Imprimir o número de nós e arestas no grafo com threshold
    num_nos = len(grafo_com_threshold.nodes())
    num_arestas = len(grafo_com_threshold.edges())
    print(f"GRAFO NORMALIZADO COM THRESHOLD ### Nós={num_nos}, Arestas={num_arestas}")
    
    return grafo_com_threshold


def inverter_pesos(grafo):
    for u, v, w in grafo.edges(data=True):
        novo_peso = 1 - w['weight']
        grafo[u][v]['weight'] = novo_peso
    print("INVERSÃO DE PESOS CONCLUÍDA !")