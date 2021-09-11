#!/usr/bin/python3
# -*- coding: utf-8 -*-
import constraintProgramming.cp_ortool_graphcoloring as cp_ortool_graphcoloring
import IteratedLocalSearch.local_search as local_search
import visualization

class Node:
    def __init__(self, index, value, color):
        self.index = index
        self.value = value
        self.color = color

    def setColor(self, color):
        self.color = color

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))


    nodesColor = [-1]*node_count
    solution = []
    
    option = input("(1)Constraint Programming: CPSAT Solver\n(2)Local Search\n>>")
    if(option =="1"): solution = cp_ortool_graphcoloring.ORToolsSolver(edges, node_count)
    if(option =="2"): solution = local_search.iterated_local_search_minimize_colors(edges, node_count)

    if(validade_solution(solution, edges)): print("Solução Validada! :)")

    if(visualization.__PLOT): visualization.plot(solution, edges, node_count)

    # prepare the solution in the specified output format
    output_data = str(max(solution)+1) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data

def validade_solution(solution, edges):
    for e in edges:
        if(solution[e[0]] == solution[e[1]]): return False
    return True

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

