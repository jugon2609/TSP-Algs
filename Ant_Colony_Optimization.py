import random
import math

def aco_tsp(graph, iterations=2000, ants_per_generation=50, alpha=1.0, beta=5.0, evaporation_rate=0.5, pheromone_deposit=10.0):
    """
    Parameters:
        graph: A dictionary where keys are nodes and values are dictionaries of neighbors and their distances.
        iterations: Number of iterations to perform.
        ants_per_generation: Number of ants in each generation.
        alpha: Influence of pheromone trails.
        beta: Influence of heuristic information (1 / distance).
        evaporation_rate: Rate at which pheromone evaporates.
        pheromone_deposit: Amount of pheromone deposited by each ant.

    Returns:   
        tuple: The best tour and its length.
    """
    pheromone = {(min(node, neighbor), max(node, neighbor)): 1.0
                 for node in graph
                 for neighbor in graph[node]}
    best_tour = None
    best_length = float('inf')
    evolist = []


    for iteration in range(iterations):
        all_tours = []
        for h in range(ants_per_generation):
            tour, length = construct_tour(graph, pheromone, alpha, beta)
            all_tours.append((tour, length))
            if length < best_length:
                evolist.append(tour)
                best_tour = tour
                best_length = length

        evaporate_pheromone(pheromone, evaporation_rate)
        for tour, length in all_tours:
            deposit_pheromone(pheromone, tour, pheromone_deposit / length)

        print(f"Iteration {iteration + 1}/{iterations}: Best length = {best_length}")

    return best_tour, best_length, evolist


def construct_tour(graph, pheromone, alpha, beta):
    snode = random.choice(list(graph.keys()))
    tour = [snode]
    uE = set(graph.keys()) - {snode}
    length = 0
    currentnode = snode

    while uE:
        probs = []
        for neighbor in uE:
            edge = (min(currentnode, neighbor), max(currentnode, neighbor))
            level = pheromone[edge]
            heuristic = 1 / graph[currentnode][neighbor]
            probs.append((level ** alpha) * (heuristic ** beta))
        probs_sum = sum(probs)
        if probs_sum == 0:
            probs = [1 / len(probs)] * len(probs)
        else:
            probs = [p / probs_sum for p in probs]

        next_node = random.choices(list(uE), weights=probs, k=1)[0]
        tour.append(next_node)
        length += graph[currentnode][next_node]
        currentnode = next_node
        uE.remove(next_node)

    length += graph[currentnode][snode]
    return tour, length


def evaporate_pheromone(pheromone, evaporation_rate):
    for edge in pheromone:
        pheromone[edge] *= (1 - evaporation_rate)
    if pheromone[edge] < 0.000000001:
            pheromone[edge] = 0.000000001


def deposit_pheromone(pheromone, tour, deposit_amount):
    for i in range(len(tour) - 1):
        edge = (min(tour[i], tour[i + 1]), max(tour[i], tour[i + 1]))
        pheromone[edge] += deposit_amount
    edge = (min(tour[-1], tour[0]), max(tour[-1], tour[0]))
    pheromone[edge] += deposit_amount


def importlist(file_path):
    with open(file_path, 'r') as file:
        coordinates = []
        for line in file:
            l = line.strip().split(',')
            x,y = float(l[0]),float(l[1])
            coordinates.append((x, y))

    graph = {}
    num_nodes = len(coordinates)
    
    for i in range(num_nodes):
        graph[coordinates[i]] = {}
        for j in range(num_nodes):
            if i != j:
                x1, y1 = coordinates[i]
                x2, y2 = coordinates[j]
                distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                graph[coordinates[i]][coordinates[j]] = distance
    return graph


def exportlist(bestt,bestl):
    filename = f"ACO_{bestl}.txt"
    with open(filename, 'w') as f:
        for i in bestt:
            f.write(f"{i[0]},{i[1]}\n")

evolist = []
def export_evo(evolist, filename):
    ret = open(filename, 'w')
    for route in evolist:
        for city in route:
            ret.write(f"{city[0]},{city[1]};")
        ret.write('\n')
    ret.close()


g = importlist("random_coordinates_120.txt")
bestt, bestl, evolist = aco_tsp(g)
exportlist(bestt,bestl)
print("Best Tour:", bestt)
print("Best Length:", bestl)
export_evo(evolist,'120_citiesevo1.txt')
#33523
#34431.56158632203 - for 48 cities