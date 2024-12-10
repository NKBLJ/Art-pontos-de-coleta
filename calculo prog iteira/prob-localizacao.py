import numpy as np
from scipy.optimize import minimize

# Dados do problema
bairros = np.array([[-5.1817395926285466, -42.77865671465523], [-5.2007093, -42.75158329999999], [-5.004638022622274, -42.82914357631114], [-4.9873352, -42.83941610000001]])  # Coordenadas dos bairros
populacoes = np.array([47901, 6593, 16970, 21923])

k = 4  # Número de novos pontos de coleta
alpha = 1.0  # Peso para a cobertura
beta = 10.0  # Peso para o espalhamento

# Calcular os limites (bounds)
x_min, x_max = bairros[:, 0].min(), bairros[:, 0].max()
y_min, y_max = bairros[:, 1].min(), bairros[:, 1].max()
bounds = [(x_min, x_max), (y_min, y_max)] * k  # Repetir para cada ponto


# Função de custo combinada
def funcao_objetivo(pontos):
    pontos = pontos.reshape((k, 2))  # Reformata para coordenadas (x, y)

    # Termo 1: Custo de cobertura
    custo_cobertura = 0
    for i, bairro in enumerate(bairros):
        distancias = np.linalg.norm(bairro - pontos, axis=1)
        custo_cobertura += populacoes[i] * np.min(distancias)

    # Termo 2: Custo de espalhamento (distância mínima entre pontos)
    distancias_pontos = []
    for j in range(k):
        for l in range(j + 1, k):
            distancias_pontos.append(np.linalg.norm(pontos[j] - pontos[l]))

    if distancias_pontos:
        custo_espalhamento = -np.min(distancias_pontos)  # Queremos maximizar, então invertido
    else:
        custo_espalhamento = 0

    # Combinação dos dois termos
    return alpha * custo_cobertura + beta * custo_espalhamento


# Configurações iniciais
pontos_iniciais = np.random.uniform(low=[x_min, y_min] * k, high=[x_max, y_max] * k)

# Otimização
resultado = minimize(funcao_objetivo, pontos_iniciais, bounds=bounds, method='L-BFGS-B')

# Resultados
pontos_otimizados = resultado.x.reshape((k, 2))
print("Coordenadas dos novos pontos de coleta:")
print(pontos_otimizados)