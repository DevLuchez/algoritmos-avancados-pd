def resolver():
    # --- ETAPA 1: PRÉ-PROCESSAMENTO DOS DADOS DE ENTRADA ---
    lista_input = []

    # Ler o arquivo entrada.txt
    with open('entrada.txt', 'r', encoding='utf-8') as arquivo_entrada:
        # Para cada linha da entrada padrão
        for linha_input in arquivo_entrada:
            # Organizar linha_input, removendo espaços/quebras de linha
            linha_limpa = linha_input.strip()

            # Se a linha_limpa não estiver vazia e não começar com #
            if linha_limpa and not linha_limpa.startswith('#'):
                # Adiciona os números da linha_limpa à lista_input, separando os índices
                lista_input.extend(linha_limpa.split())

    # Se a lista do input estiver vazia, exibir mensagem de erro e finalizar o programa
    if not lista_input:
        print('Entrada vazia!')
        return

    # --- ETAPA 2: MODELAGEM DA ESTRUTURA DE DADOS DO GRAFO ---
    # Ler o número de vértices do grafo, vindo da lista_input
    numero_vertices = int(lista_input[0])

    # Ler a Matriz de Adjacência, vinda da lista_input
    matriz_adjacencia = []
    indice_entrada = 1      # Definir o início da matriz inserida na entrada

    """
    Composição da matriz:
    - Linha da matriz -> Vértice de origem do grafo
    - Coluna da matriz -> Vértice de destino do grafo
    - matriz[linha][coluna] -> Peso da aresta entre os dois vértices
    """

    # Para cada linha da matriz (vértice de origem)
    for linha in range(numero_vertices):
        # Inicializar lista vazia para construir a linha atual da matriz
        linha_atual = []
        # Para cada coluna da matriz (vértice de destino)
        for coluna in range(numero_vertices):
            # Adicionar na linha_atual o peso da aresta entre o vértice de origem e o vértice de destino (a partir do indice_entrada atual)
            linha_atual.append(int(lista_input[indice_entrada]))
            indice_entrada += 1

        # Adicionar na matriz_adjacencia os pesos das arestas entre todos os vértices (a partir da linha_atual)
        matriz_adjacencia.append(linha_atual)

    # Ler vértices de origem e destino do grafo, bem como o limite de vértices a visitar
    vertice_origem = int(lista_input[indice_entrada])       # Vértice de origem inserido na entrada
    vertice_destino = int(lista_input[indice_entrada + 1])  # Vértice de destino inserido na entrada
    limite_vertices = int(lista_input[indice_entrada + 2])  # Limite de vértices inserido na entrada (restrição k)

    # --- ETAPA 3: BUSCA PELO CAMINHO DE MAIOR PESO - ALGORITMO DE PROGRAMAÇÃO DINÂMICA (DFS COM MEMOIZAÇÃO) ---
    # Inicializar dicionário de memoização para armazenar (vertice_atual, qtde_visitados) e evitar reprocessamento de subproblemas já resolvidos
    cache_subproblemas = {}

    # Função recursiva para encontrar o caminho de maior peso entre vertice_origem e vertice_destino, respeitando o limite_vertices
    def buscar_caminho_maximo(vertice_atual, qtde_vertices_visitados):
        """
         Busca recursivamente uma solução ótima para todos os subproblemas e,
         então retorna a melhor solução ótima para o problema representado no grafo.

         Caso encontre uma solução ótima para todos os subproblemas, ele retorna uma
         tupla para a solução do problema global através de uma tupla (maior_peso, maior_caminho):
                 - peso_maximo: soma dos pesos das arestas do melhor caminho
                 - caminho: lista de vértices que formam o melhor caminho

         Caso não encontre solução ótima para nenhum dos subproblemas, retorna (-infinito, []).
         """

        # Caso base 1: Chegou ao destino
        if vertice_atual == vertice_destino:
            return 0, [vertice_atual]                   # O peso do vertice atual para o vertice destino é 0 (por exemplo, do 4 para o 4 não há arestas)

        # Caso base 2: Não chegou ao destino e atingiu o limite de vértices (restrição k)
        if qtde_vertices_visitados == limite_vertices:
            return float('-inf'), []                    # É impossível chegar ao vertice_destino com o limite_vertices definido

        # Armazena o estado_atual do vértice
        estado_atual = (vertice_atual, qtde_vertices_visitados)
        # Se já houver uma solução ótima para subproblema atual (estado_atual do vértice)
        if estado_atual in cache_subproblemas:
            return cache_subproblemas[estado_atual]     # Retorna subproblema já resolvido

        # Inicializar melhor_peso e melhor_caminho para o subproblema atual
        melhor_peso = float('-inf')
        melhor_caminho = []

        # Para cada vertice_vizinho (vértice ligado ao vértice atual)
        for vertice_vizinho in range(numero_vertices):
            # Armazenar peso da aresta entre o vertice_atual e o vértice ligado a ele
            peso_aresta = matriz_adjacencia[vertice_atual][vertice_vizinho]

            # Se a aresta entre os vértices não possui peso, pula para o próximo vertice_vizinho
            if peso_aresta == 0:
                continue

            # Chamar a própria função para analisar recursivamente o peso de todas as arestas e os caminhos entre todos os vértices do grafo
            peso_a_partir_do_vizinho, caminho_a_partir_do_vizinho = buscar_caminho_maximo(vertice_vizinho, qtde_vertices_visitados + 1)

            # Se o caminho explorado chegou ao vertice_destino
            if peso_a_partir_do_vizinho != float('-inf'):
                # Calcular o peso acumulado entre os vértices explorados
                peso_caminho_completo = peso_aresta + peso_a_partir_do_vizinho

                # Se o caminho atual possui um peso maior que o melhor_peso anterior
                if peso_caminho_completo > melhor_peso:
                    melhor_peso = peso_caminho_completo                             # Atualizar melhor_peso
                    melhor_caminho = [vertice_atual] + caminho_a_partir_do_vizinho  # Atualizar melhor_caminho

        # Armazenar o melhor resultado no estado do vértice atual
        cache_subproblemas[estado_atual] = (melhor_peso, melhor_caminho)
        # Retornar o peso acumulado e maior caminho
        return melhor_peso, melhor_caminho

    # --- ETAPA 4: EXECUÇÃO E SAÍDA ---
    # Chamar a função recursiva a partir do vertice_origem e da qtde_vertices_visitados atual
    peso_maximo, caminho_encontrado = buscar_caminho_maximo(vertice_origem, 1)

    # Se a função recursiva tiver finalizado a partir do caso de base 2, não existe caminho válido
    if peso_maximo == float('-inf'):
        # Informar que é impossível chegar ao vertice_destino com o limite_vertices definido
        print("Não existe caminho válido.")
    else:
        # Exibir output, informando o melhor caminho, o peso acumulado e o total de vértices visitados
        print(f"Caminho máximo: {caminho_encontrado}")
        print(f"Peso total: {peso_maximo}")
        print(f"Número de vértices no caminho: {len(caminho_encontrado)}")


# Execução principal do script
if __name__ == '__main__':
    resolver()