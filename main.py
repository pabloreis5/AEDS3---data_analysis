from func import *


year = int(input("Digite o ano de interesse: "))

politicians_file = "datasets/politicians{year}.csv"
graph_file = "datasets/graph2022{year}.csv"

# Criar o grafo
grafo = criar_grafo(politicians_file, graph_file)

# # Aplicar filtros
# ano_filtrado = 2022
# partidos_filtrados = ['PT', 'PL', 'MDB']
# aplicar_filtros(grafo, ano=ano_filtrado, partidos=partidos_filtrados)

# # Normalizar pesos
# normalizar_pesos(grafo)

# # Remover arestas pouco significativas
# threshold = 0.1  # Defina o threshold desejado
# remover_arestas_pouco_significativas(grafo, threshold)

# # Inverter pesos
# inverter_pesos(grafo)

# # Calcular a centralidade de betweenness
# centralidade = calcular_centralidade_betweenness(grafo)

# # Plotar o gráfico de barras da centralidade
# plotar_grafico_centralidade(centralidade)
