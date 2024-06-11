import math
import random
import sys
from common import print_tour, read_input
import matplotlib.pyplot as plt

# 都市の座標
cities=read_input(sys.argv[1])

# 2点間の距離を計算する関数
def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)

# 経路の総距離を計算する関数
def total_distance(route):
    dist = 0
    for i in range(len(route)):
        dist += distance(cities[route[i]], cities[route[(i+1) % len(route)]])
    return dist

# 適応度を計算する関数 (総距離の逆数)
def fitness(route):
    return 1 / total_distance(route)

# 交叉操作
def crossover(parent1, parent2):
    child = [-1] * len(parent1)
    start = random.randint(0, len(parent1)-1)
    end = random.randint(0, len(parent1)-1)
    if start > end:
        start, end = end, start
    for i in range(start, end+1):
        child[i] = parent1[i]
    child_pos = (end + 1) % len(child)
    for city in parent2:
        if city not in child:
            child[child_pos] = city
            child_pos = (child_pos + 1) % len(child)
    return child

# 突然変異操作
def mutate(route):
    pos1 = random.randint(0, len(route)-1)
    pos2 = random.randint(0, len(route)-1)
    route[pos1], route[pos2] = route[pos2], route[pos1]
    return route



# 遺伝子アルゴリズム
def genetic_algorithm(population_size, num_generations,cities):
    x_generation = []
    y_total_distance = []
    population = [list(range(len(cities))) for _ in range(population_size)]
    best_route = min(population, key=total_distance)
    for generation in range(num_generations):
        population = sorted(population, key=fitness, reverse=True)
        print(f"世代 {generation+1}")
        # print(f"現在の最良経路 = {[cities[i] for i in population[0]]}, 総距離 = {total_distance(population[0])}")
        # print(f"最良経路 (この時点での) = {[cities[i] for i in best_route]}, 総距離 = {total_distance(best_route)}")
        print(f"総距離 = {total_distance(best_route)}")
        x_generation.append(generation+1)
        y_total_distance.append(total_distance(best_route))
        new_population = []
        elite = population[:2]  # エリート選択
        new_population.extend(elite)
        while len(new_population) < population_size:
            parent1 = random.choice(population[:population_size//2])
            parent2 = random.choice(population[:population_size//2])
            child = crossover(parent1, parent2)
            new_population.append(mutate(child))
        population = new_population
        best_route = min(population, key=total_distance)
    # print(x_generation)
    # print(y_total_distance)
    plt.plot(x_generation, y_total_distance, marker='.',)
    plt.title(sys.argv[1],fontsize=15)
    plt.show()
    return best_route

# 実行
if __name__ == '__main__':
    assert len(sys.argv) > 2
    best_route = genetic_algorithm(population_size=100, num_generations=10000, cities=read_input(sys.argv[1]))
    print(f"\n最終の最良経路:")
    print_tour(best_route)
    print(f"総距離: {total_distance(best_route)}")
    number = sys.argv[2]
    f = open('output_' + number +'.csv', 'w')
    f.write('index\n')
    for i in best_route:
        f.write(f'{i}\n')
    f.close()

