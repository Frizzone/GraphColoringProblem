import random
from datetime import datetime
import IteratedLocalSearch.graph_matrix as solution
import visualization
    

def create_greedy_solution(edges, node_count, rand):
    graph_matrix = solution.GraphColoringSolution(node_count, edges)
    max_color = 0
    for node in range(node_count):
        neighborhood_colors = graph_matrix.get_neighborhood_colors(node)
        all_colors = set(range(0, max_color+2))
        possible_colors = all_colors.symmetric_difference(neighborhood_colors)
        if(not rand or len(possible_colors) == 1): color = list(possible_colors)[0]
        else: color = random.choice(list(possible_colors)[:-1])
        graph_matrix.update_node_color(node, color, update_conflict_node=False)
        max_color = max(color, max_color)
    return (graph_matrix, max_color)

def multi_start_greedy(edges, node_count):
    max_it = 20
    (best_greedy_matrix, best_max_color) = create_greedy_solution(edges, node_count, False)
    print(datetime.now().strftime('%d/%m/%Y %H:%M:%S') + ": greedy# Número de Cores = " + str(best_max_color+1) + " na iteração 0")
    for i in range(max_it):
        (greedy_matrix, max_color) = create_greedy_solution(edges, node_count, True)
        if(max_color < best_max_color):
            best_greedy_matrix = greedy_matrix
            best_max_color = max_color
            print(datetime.now().strftime('%d/%m/%Y %H:%M:%S') + ": greedy# Número de Cores = " + str(best_max_color+1) + " na iteração " + str(i))
    best_greedy_matrix.init_color_list()
    return (best_greedy_matrix, best_max_color)

def local_search_best_improvement(graph_matrix:solution.GraphColoringSolution):
    improvement = True
    while (improvement):
        improvement = False
        best_node = 0
        best_color = 0
        best_value = 0
        #best improvement: get the best color and node (minimize the conflicts)
        for node in range(graph_matrix.node_count):
            if(not graph_matrix.is_conflicted(node)): continue
            for color in graph_matrix.color_list:
                value = 0
                if(graph_matrix.get_color(node) != color): value = graph_matrix.evaluate_new_solution(node, color)
                if(value < best_value):
                    best_node = node
                    best_color = color
                    best_value = value
        #if the solution is a improvement
        if(best_value < 0):
            improvement = True
            graph_matrix.update_node_color(best_node, best_color, update_conflict_node=True)
    print(datetime.now().strftime('%d/%m/%Y %H:%M:%S') + ": local_search# FO = " + str(graph_matrix.sum_conflicts_object_function_value()))
    return graph_matrix.is_feasible()

def iterated_local_search_minimize_colors(edges, node_count):
    max_it = 100
    (graph_matrix, max_color) = multi_start_greedy(edges, node_count)
    current_solution = graph_matrix.get_solution()
    feasible = True
    max_color-=1
    while(feasible):
        print(datetime.now().strftime('%d/%m/%Y %H:%M:%S') + ": local_search_minimize_colors# Reduzindo número de cores = " + str(max_color+1))
        graph_matrix.reduce_color()
        for i in range(max_it):
            feasible = local_search_best_improvement(graph_matrix)
            if (feasible): 
                current_solution =  graph_matrix.get_solution()
                print(datetime.now().strftime('%d/%m/%Y %H:%M:%S') + ": local_search_minimize_colors# Achou solução com número de cores = " + str(max_color+1) + " após " + str(i) + " iterações")
                break
            else:
                pertubation(graph_matrix)
        max_color = max_color - 1
    print(datetime.now().strftime('%d/%m/%Y %H:%M:%S') + ": Finalizando Meta-Heurística")
    return current_solution

def pertubation(graph_matrix:solution.GraphColoringSolution):
    for node in range(graph_matrix.node_count):
        neighborhood_colors = graph_matrix.get_neighborhood_colors(node)
        all_colors = set(graph_matrix.color_list)
        possible_colors = all_colors.symmetric_difference(neighborhood_colors)
        if(len(possible_colors) >= 1): 
            color = random.choice(list(possible_colors))
            graph_matrix.update_node_color(node, color, update_conflict_node=True)
    return graph_matrix