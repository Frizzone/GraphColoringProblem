import random

class GraphColoringSolution:
    NO_CONFLICT = 0
    CONFLICT = 1
    NO_EDGE = -1

    def set_solution(self, solution):
        self.colors = solution
        self.update_graph_matrix()
        self.update_conflitct_list()
        self.init_color_list()

    def get_solution(self):
        solution = []
        for c in self.colors:
            solution.append(self.color_list.index(c))
        return solution
    
    def get_color(self, node):
        return self.colors[node]

    def is_conflicted(self, node):
        return (self.conflict_node_list[node] == GraphColoringSolution.CONFLICT)

    def is_feasible(self):
        for edge in self.edges:
            if(self.graph_matrix[edge[0]][edge[1]] == GraphColoringSolution.CONFLICT): return False
        return True

    def __init__(self, node_count, edges):
        self.edges = edges
        self.node_count = node_count
        self.graph_matrix = self.__init_graph_matrix()
        self.colors = [0]*node_count
        self.conflict_node_list = [0]*node_count
        self.color_list = list()

    #initialize graph matrix representation
    def __init_graph_matrix(self):
        graph_matrix = [[GraphColoringSolution.NO_EDGE for x in range(self.node_count)] for y in range(self.node_count)]
        for edge in self.edges:
            graph_matrix[edge[0]][edge[1]] = GraphColoringSolution.NO_CONFLICT
            graph_matrix[edge[1]][edge[0]] = GraphColoringSolution.NO_CONFLICT
        return graph_matrix

    #update graph matrix representation
    def update_graph_matrix(self):
        for edge in self.edges:
            self.graph_matrix[edge[0]][edge[1]] = (self.colors[edge[0]] == self.colors[edge[1]])
            self.graph_matrix[edge[1]][edge[0]] = (self.colors[edge[0]] == self.colors[edge[1]])
    
    #update list of colors with conflict
    def update_conflitct_list(self):
        for node in range(self.node_count):
            for nodeto in range(self.node_count):
                if(self.graph_matrix[node][nodeto] != GraphColoringSolution.NO_EDGE and self.colors[node] == self.colors[nodeto]):
                    self.conflict_node_list[node] = GraphColoringSolution.CONFLICT
                    break
    
    #initialize color list
    def init_color_list(self):
        self.color_list = list(range(0, max(self.colors)+1))

    #return a set of colors of nodes adjacents
    def get_neighborhood_colors(self, node):
        colors = []
        for nodeto in range(self.node_count): 
            if(self.graph_matrix[node][nodeto] == GraphColoringSolution.NO_CONFLICT): colors.append(self.colors[nodeto])
        return set(colors)

    #change node color
    def update_node_color(self, node, color, update_conflict_node):
        self.colors[node] = color
        if(update_conflict_node): self.__update_conflict_node(node)

    #update the conflicts control, after the node color change
    def __update_conflict_node(self, node):
        self.conflict_node_list[node] = False
        for nodeto in range(self.node_count):
            if(self.graph_matrix[node][nodeto] != GraphColoringSolution.NO_EDGE):
                self.graph_matrix[node][nodeto] = (self.colors[node] == self.colors[nodeto])
                self.graph_matrix[nodeto][node] = (self.colors[node] == self.colors[nodeto])
                if(not self.conflict_node_list[node] and (self.colors[node] == self.colors[nodeto])): self.conflict_node_list[node] = True

    #if one node change to a color, evaluate solution in terms o conflict reduction
    def evaluate_new_solution(self, node, color):
        delta_value = 0
        for nodeto in range(self.node_count):
            if(self.graph_matrix[node][nodeto] == GraphColoringSolution.NO_CONFLICT
            and color == self.colors[nodeto]):
                delta_value+=1
            if(self.graph_matrix[node][nodeto] == GraphColoringSolution.CONFLICT 
            and color != self.colors[nodeto]):
                delta_value-=1
        return delta_value
    
    def sum_conflicts_object_function_value(self):
        value = 0
        for edge in self.edges: 
            if(self.graph_matrix[edge[0]][edge[1]] == GraphColoringSolution.CONFLICT): value+=1
        return value

    def reduce_color(self):
        color_remove = random.choice(self.color_list)
        self.color_list.remove(color_remove)
        color_swap = random.choice(self.color_list)
        self.swap_color(color_remove, color_swap)
        return self

    def swap_color(self, color, new_color):
        for node in range(self.node_count):
            if(self.colors[node] == color): self.update_node_color(node, new_color, update_conflict_node=True)