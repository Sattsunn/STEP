import math
import random
import sys
import time
import random
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

# 2.5opt
def two_point_five_opt(route, cities):
    two_opt_start_time = time.time()
    # 距離のキャッシュを初期化
    distance_cache = {}
    for i in range(len(cities)):
        for j in range(i + 1, len(cities)):
            distance_cache[(i, j)] = distance(cities[i], cities[j])
            distance_cache[(j, i)] = distance_cache[(i, j)]

    best_distance = total_distance(route)
    improved = True
    while improved:
        improved = False
        for i in range(len(route) - 2):
            for j in range(i + 2, len(route)):
                if j - i == 1: continue  # 隣接する点はスキップ

                # キャッシュから距離を取得
                old_distance = distance_cache[(route[i], route[i + 1])] + distance_cache[(route[j], route[(j + 1) % len(route)])]
                new_distance = distance_cache[(route[i], route[j])] + distance_cache[(route[i + 1], route[(j + 1) % len(route)])]

                if new_distance < old_distance:
                    route[i + 1:j + 1] = reversed(route[i + 1:j + 1])
                    best_distance -= old_distance - new_distance
                    improved = True
                    break
            if improved:
                break
    two_opt_end_time = time.time() 
    print(f"実行時間: {two_opt_end_time - two_opt_start_time} 秒")  
    return route

# 貪欲法
def greedy(cities):
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    return tour

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
def genetic_algorithm(population_size, num_generations, cities):
    x_generation = []
    y_total_distance = []
    # 初期経路を初期集団に全てgreedyから生成
    population = [greedy(cities) for _ in range(population_size)]  
    best_route = min(population, key=total_distance)
    for generation in range(num_generations):
        population = sorted(population, key=fitness, reverse=True)
        print(f"世代 {generation+1}, 最も短い総距離 = {total_distance(best_route)}")
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
        new_population = [two_point_five_opt(individual,cities) for individual in new_population]
        current_best_route = min(new_population, key=total_distance)
        if total_distance(current_best_route) < total_distance(best_route):
            best_route = current_best_route
            output_route(best_route)
    plt.plot(x_generation, y_total_distance, marker='.')
    plt.title(sys.argv[1],fontsize=15)
    plt.show()
    return best_route

def output_route(route):
    number = sys.argv[2]
    f = open('output_' + number +'.csv', 'w')
    f.write('index\n')
    for i in route:
        f.write(f'{i}\n')
    f.close()

# 実行
if __name__ == '__main__':
    assert len(sys.argv) > 2
    start_time = time.time()

    best_route = genetic_algorithm(population_size=5, num_generations=100, cities=read_input(sys.argv[1]))
    print(f"\n最終の最良経路:")
    print_tour(best_route)
    print(f"総距離: {total_distance(best_route)}")
    output_route(best_route)

    end_time = time.time() 
    print(f"実行時間: {end_time - start_time} 秒")  

