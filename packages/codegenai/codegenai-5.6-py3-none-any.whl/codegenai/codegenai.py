from codegenai.aids import *


code = """
import networkx as nx
import matplotlib.pyplot as plt

def pretty_print(graph, title = "Graph Visualization",weighted = False, directed = False, heuristic = None):
    g = nx.DiGraph() if directed else nx.Graph()
    for u in graph:
        label = u
        if heuristic:
            label += "("+str(heuristic[u])+")"
        g.add_node(u, label = label)
        for v in graph[u]:
            g.add_edge(u, v, weight = graph[u][v])
    pos = nx.circular_layout(g)
    nx.draw(g, pos, 
            node_size = 1200, node_color = 'lightgreen',
            width = 1.5, edge_color = 'red',
            edgecolors = 'black', linewidths = 1.5,
            margins = 0.25, clip_on = False)
    nx.draw_networkx_labels(g, pos, labels = nx.get_node_attributes(g, 'label'),
                            font_size = 12, font_family = 'cursive')
    if weighted:
        nx.draw_networkx_edge_labels(g, pos, 
                                     edge_labels = nx.get_edge_attributes(g, 'weight'),
                                     font_size = 8, font_family = 'cursive')
    plt.suptitle(title)
    plt.axis('off')
    plt.show()
    plt.clf()

#______________________________________________

def display(graph):
    g = nx.DiGraph()
    for u in graph:
        g.add_node(u)
        for v in graph[u]:
            g.add_edge(u, v, weight = graph[u][v])
    pos = nx.circular_layout(g)
    nx.draw(g, pos, with_labels = True)
    nx.draw_networkx_edge_labels(g, pos, edge_labels = nx.get_edge_attributes(g, 'weight'))
    plt.show()
    plt.clf()

#______________________________________________

def get_input(heuristic = False, weighted = False, bound = False, directed = False):
    rtn = []
    graph = {}
    rtn.append(graph)
    if heuristic:
        h = {}
        for _ in range(int(input("Enter no of nodes: "))):
            x, hval = input("Enter node and heuristic value: ").split()
            h[x] = int(hval)
        rtn.append(h)
    for _ in range(int(input("Enter no of edges: "))):
        if weighted:
            u, v, w = input("Enter (node, adj, weight): ").split()
        else:
            u, v = input("Enter (node, adj): ").split()
            w = 0
        graph[u] = graph.get(u,{})
        graph[u][v] = int(w)
        graph[v] = graph.get(v,{})
        if not directed:
            graph[v][u] = int(w)
    source, goal = input("Enter source and goal: ").split()
    if bound:
        b = int(input("Enter memory bound: "))
        rtn.append(b)
    rtn.extend([source, goal])
    return rtn

#______________________________________________

def print_path(node, parent):
    if node != None:
        return print_path(parent[node], parent) + [node]
    return []


def BFS(graph, start, goal):
    queue = [start]
    visited = []
    parent = {start : None}
    while queue:
        node = queue.pop(0)#First element
        visited.append(node)
        if node == goal:
            print("Result(BFS):",print_path(node, parent))
            return True
        for adj in graph[node]:
            if adj not in visited and adj not in queue:
                queue.append(adj)
                parent[adj] = node
    return False

#______________________________________________

def DFS(graph, start, goal):
    stack = [start]
    visited = []
    parent = {start : None}
    while stack:
        node = stack.pop()#last element
        visited.append(node)
        if node == goal:
            print("Result(DFS):",print_path(node, parent))
            return True
        for adj in graph[node]:
            if adj not in visited and adj not in stack:
                stack.append(adj)
                parent[adj] = node
    return False

#______________________________________________

def UCS(graph, start, goal):
    queue = [start]
    visited = []
    parent = {start : None}
    cost = {start : 0}
    while queue:
        queue.sort(key = lambda x : cost[x])
        node = queue.pop(0)
        visited.append(node)
        if node == goal:
            print("Result(UCS):",print_path(node, parent),"Path cost =",cost[node])
            return True
        for adj in graph[node]:
            if adj not in visited:
                new_cost = cost[node] + graph[node][adj]
                if adj not in queue:
                    queue.append(adj)
                elif new_cost > cost[adj]:
                    continue
                cost[adj] = new_cost
                parent[adj] = node
    return False

#______________________________________________

def DLS(graph, start, goal, limit):
    result = recursive_dls(graph, start, goal, limit, [start])
    print("Result(DLS):",result)


def recursive_dls(graph, node, goal, limit, visited):
    if node == goal:
        return [node]
    elif limit == 0:
        return 'cutoff'
    else:
        status = 'failure'
        for adj in graph[node]:
            if adj not in visited:
                visited.append(adj)
                result = recursive_dls(graph, adj, goal, limit - 1, visited)
                if result == 'cutoff':
                    status = 'cutoff'
                    visited.remove(adj)
                elif result != 'failure':
                    return [node] + result
        return status
        
#______________________________________________

def IDS(graph, start, goal):
    depth = 0
    while True:
        result = recursive_dls(graph, start, goal, depth, [start])
        print("Result(IDS/IDDFS):",result,"at depth limit =",depth)
        if result != 'cutoff':
            return
        depth += 1

#______________________________________________

def AStar(graph, start, goal, h):
    queue = [start]
    visited = []
    parent = {start : None}
    g = {start : 0}
    f = {start : h[start]}
    while queue:
        queue.sort(key = lambda x : f[x])
        node = queue.pop(0)
        visited.append(node)
        if node == goal:
            print("Result(A*):",print_path(node, parent),"Path cost =",g[node])
            return True
        for adj in graph[node]:
            if adj not in visited:
                gcost = g[node] + graph[node][adj]
                fcost = gcost + h[adj]
                if adj not in queue:
                    queue.append(adj)
                elif fcost > f[adj]:
                    continue
                g[adj] = gcost
                f[adj] = fcost
                parent[adj] = node
    return False

#______________________________________________

def IDAStar(graph, start, goal, h):
    def dfs(graph, parent, node, goal, g, h, th):
        f = g + h[node]
        if f > th:
            return None, f
        if node == goal:
            return node, f
        min_th = inf
        for adj in graph[node]:
            result, temp_th = dfs(graph, parent, adj, goal, g + graph[node][adj], h, th)
            if result is not None:
                parent[adj] = node
                return result, temp_th
            elif temp_th < min_th:
                min_th = temp_th
        return None, min_th
    
    inf = 9999999
    parent = {start : None}    
    th = h[start]
    while True:
        result, new_th = dfs(graph, parent, start, goal, 0, h, th)
        if result is not None:
            result = print_path(result, parent)
            cost = sum([graph[n1][n2] for n1, n2 in zip(result,result[1:])])
            print("Result(IDA*):",result,"Path cost =",cost)
            return
        elif new_th == inf:
            print("Result(IDA*): failure")
            return
        th = new_th

#______________________________________________

def SMAStar(graph, start, goal, h, bound):
    queue = [start]
    visited = []
    parent = {start : None}
    g = {start : 0}
    f = {start : h[start]}
    backup = {}
    while queue:
        queue.sort(key = lambda x : f[x])
        node = queue.pop(0)
        visited.append(node)
        if node == goal:
            print("Result(SMA*):",print_path(node, parent),"Path cost =",g[node])
            return True
        successors = []
        for adj in graph[node]:
            if adj in visited:
                continue
            gcost = g[node] + graph[node][adj]
            fcost = gcost + h[adj]
            if adj in queue:
                if fcost >= f[adj]:
                    continue
            elif len(queue) < bound:
                    queue.append(adj)
            else:
                worst = max(queue, key = lambda x : f[x])
                if fcost < f[worst]:
                    backup[worst] = f[worst]
                    queue.remove(worst)
                    queue.append(adj)
                else:
                    continue
            g[adj] = gcost
            f[adj] = fcost
            parent[adj] = node
            successors.append(adj)
        if not successors and node in backup:
            f[node] = backup[node]
        elif not successors:
            f[node] = float('inf')
    return False

#______________________________________________

from random import randint as rint
def genetic(gen, pop):
    def show(b):
        board = [ ['_'] * n for _ in range(n)]
        for i in range(n):
            board[int(b[i])-1][i] = 'Q'
        print(f" {' '.join(['_']*n)}")
        for i in board:
            print(f"|{'|'.join(i)}|")
    def mutate(b1, b2):
        b1, b2 = list(b1), list(b2)
        x, y = rint(0,n-1), rint(0,n-1)
        b1[x], b2[x] = b2[x], b1[x]
        b1[y] = str(int(y) + 1)
        return (''.join(b1),''.join(b2))
    def crossover(b1, b2):
        b1, b2 = list(b1), list(b2)
        x = rint(1,n-1)
        b1[0:x], b2[0:x] = b2[0:x], b1[0:x]
        return (''.join(b1), ''.join(b2))
    def fitness(b):
        b = list(b)
        attacks = 0
        for i in range(n):
            for j in range(i+1, n):
                if b[i] == b[j] or abs(int(b[i]) - int(b[j])) == j - i:
                    attacks += 1
        return attacks
    n = len(pop[0])
    i = 0
    pq = []
    pq.append((fitness(pop[0]),pop[0]))
    pq.append((fitness(pop[1]),pop[1]))
    for i in range(gen+1):
        f1, b1 = pq.pop(0)
        f2, b2 = pq.pop(0)
        pq.clear()
        if f1 == 0:
            print("Goal State:",b1,"Generation:",i+1)
            show(b1)
            return
        elif f2 == 0:
            print("Goal State:",b2,"Generation:",i+1)
            show(b2)
            return
        x1, x2 = crossover(b1, b2)
        x3, x4 = crossover(b2, b1)
        new_pop = [(x1, x2), (x3, x4), mutate(x1, x2), mutate(x2, x1)]
        for child in new_pop:
            pq.append((fitness(child[0]), child[0]))
            pq.append((fitness(child[1]), child[1]))
        pq.append((f1, b1))
        pq.append((f2, b2))
        pq.sort(key = lambda x : x[0])
    print("Most Evolved State:",pq[0][1],"Generation:",i,"Attacks:",pq[0][0])
    show(pq[0][1])

#______________________________________________

import math
import random
def simulated_annealing(initsol, inittemp, alpha, iters):
    def fcost(sol):
        return sum([i**2 for i in sol])
    def successors(sol, step = 1.0):
        succ = [x + random.uniform(-step,step) for x in sol]
        return succ
    currsol = initsol
    cost = fcost(currsol)
    sol = currsol
    mincost = cost
    temp = inittemp
    for iteration in range(iters):
        neighbor = successors(currsol)
        ncost = fcost(neighbor)
        costdiff = ncost - cost
        if costdiff < 0 or random.random() < math.exp(-costdiff/temp):
            currsol = neighbor
            cost = ncost
            if cost < mincost:
                sol = currsol
                mincost = cost
        temp *= alpha
    return sol, mincost

#______________________________________________

import math 
import random
def sudoku_simulated_annealing(board, initial_temp = 1.0, cooling_rate = 0.99, min_temp = 0.001):
    def display(board):
        for row in board:
            print(' '.join(str(num) if num != 0 else '.' for num in row))
        print()
    def fill(board):
        for i in range(9):
            choices = list(set(range(1,10)) - set(board[i]) - {0})
            random.shuffle(choices)
            for j in range(9):
                if board[i][j] == 0:
                    board[i][j] = choices.pop()
    def cost(board):
        conflicts = 0
        for n in range(9):
            row = board[n]
            col = [x[n] for x in board]
            conflicts += len(row) - len(set(row))
            conflicts += len(col) - len(set(col))
        for l in [0,3,6]:
            for k in [0,3,6]:
                block = []
                for i in range(0+l,3+l):
                    for j in range(0+k,3+k):
                        block.append(board[i][j])
                conflicts += 9 - len(set(block))
        return conflicts
    def next(board, fixed):
        neighbor = [[x for x in row] for row in board]
        i = random.randint(0,8)
        cols = [j for j in range(9) if (i,j) not in fixed]
        if len(cols) >= 2:
            j1, j2 = random.sample(cols, 2)
            neighbor[i][j1], neighbor[i][j2] = neighbor[i][j2], neighbor[i][j1]
        return neighbor
    fixed = [(x,y) for x in range(9) for y in range(9) if board[x][y] != 0]
    fill(board)
    current = best = board
    temp = initial_temp
    while temp > min_temp:
        neighbor = next(current,fixed)
        delta = cost(neighbor) - cost(current)
        if delta < 0:
            current = neighbor
            if cost(neighbor) < cost(best):
                best = neighbor
        else:
            if random.random() < math.exp(-delta/temp):
                current = neighbor
        temp *= cooling_rate
    print(f"Sudoku ({'Best Possible State | Attacks = '+str(cost(best)) if cost(best) else 'Solved'})") 
    display(best)

#______________________________________________

import networkx as nx
import matplotlib.pyplot as plt
def show_tree(graph):
    graph = {node : [adj for adj in graph[node]] for node in graph}
    terminal_nodes = set()
    for node in graph:
        for i in range(len(graph[node])):
            x = str(graph[node][i])
            if x.isdigit():
                while x in terminal_nodes:
                    x+=" "
                graph[node][i] = x
                terminal_nodes.add(x)
    g = nx.DiGraph(graph)
    levels = nx.single_source_shortest_path_length(g, next(iter(g.nodes)))
    layers = {}
    for node, level in levels.items():
        layers[level] = layers.get(level, []) + [node]
    pos = {}
    for level, nodes in layers.items():
        x_offset = (len(nodes) - 1)/2
        for i, node in enumerate(nodes):
            x = i - x_offset
            y = -level
            pos[node] = (x,y)
    plt.figure(figsize = (8,4))
    nx.draw(g, pos, with_labels = True, 
            node_size = 600, node_color = 'lightgreen',
            font_size = 12, font_family = 'cursive',
            arrows = False, width = 1.5, edge_color = 'red',
            edgecolors = 'black', linewidths = 1.5,
            margins = 0.1, clip_on = False)
    plt.suptitle("Alpha Beta Pruning")
    plt.show()
    plt.clf()
MIN = -float('inf')
MAX = float('inf')
def alphabeta(node, graph, ismax, pruned = [], alpha = MIN, beta = MAX, path = {}):
    if str(node).isdigit():
        return int(node), pruned, path
    option = MIN if ismax else MAX
    for child in graph[node]:
        val, _, _ = alphabeta(child, graph, not ismax, pruned, alpha, beta, path)
        if ismax:
            option = max(option, val)
            alpha = max(option, alpha)
            path[node] = alpha
        else:
            option = min(option, val)
            beta = min(option, beta)
            path[node] = beta
        if alpha >= beta:
            i = graph[node].index(child)+1
            pruned += [f"{node}-{adj}" for adj in graph[node][i:]]
            break
    return option, pruned, path
def show_path(node, graph, path, value):
    for adj in graph[node]:
        if str(adj).isdigit():
            return [node,str(value)]
        if path[adj] == value:
            return [node] + show_path(adj, graph, path, value)

#______________________________________________

import networkx as nx
import matplotlib.pyplot as plt

def backtrack_map(graph, colors):
    def rec_backtrack(assign, graph, colors):
        if -1 not in assign.values():
            return assign
        node = [x for x in assign if assign[x] == -1][0]
        for color in colors:
            if all(assign[adj] != color for adj in graph[node]):
                assign[node] = color
                result = rec_backtrack(assign, graph, colors)
                if result:
                    return result
                assign[node] = -1
        return None

    assign = {node : -1 for node in graph}
    return rec_backtrack(assign, graph, colors)
def display_map(graph, colors = None):
    g = nx.DiGraph(graph)
    #nx.draw_circular(g, with_labels = True, node_color = colors)
    nx.draw_circular(g, with_labels = True,
                    node_size = 600, node_color = colors,
                    font_size = 12, font_family = 'cursive',
                    arrows = False, width = 1.25,
                    edgecolors = 'black', linewidths = 1.5,
                    margins = 0.375, clip_on = False)
    plt.suptitle("Map Coloring(Constraint Satisfaction Problem)")
    plt.show()
    plt.clf()

#______________________________________________

import networkx as nx
import matplotlib.pyplot as plt

def backtrack_house(houses, locs):
    def check(assign, loc):
        #constraints given in the question
        #change it accordinly
    
        a = assign['A']
        b = assign['B']
        c = assign['C']
        d = assign['D']
        
        #1. C lives in a house higher than D
        if c != -1 and d != -1 and c < d:return False
    
        #2. D lives next to A in Lower number House
        if d != -1 and a != -1 and (a - d) != 1:return False
    
        #3. There is at least one house between D and B    
        if d != -1 and b != -1 and abs(d - b) == 1:return False
    
        #4. C doesn't live in house number 3
        if c != -1 and c == 3:return False
    
        #5. B doesn't live in house number 1
        if b != -1 and b == 1:return False
            
        if loc in assign.values():
            return False
        return True
    def rec_backtrack(assign, locs):
        if check(assign, -1):
            return assign
        choices = [x for x in assign if assign[x] == -1]
        house = choices[0] if choices else None
        for loc in locs:
            if check(assign, loc):
                assign[house] = loc
                res = rec_backtrack(assign, locs)
                if res:
                    return res
                assign[house] = -1
        return None

    assign = {house : -1 for house in houses}    
    return rec_backtrack(assign, locs)
def display_house(result):
    g = nx.Graph()
    nodes = list(result.keys())
    nodes.sort(key = lambda x : result[x])
    nodes = [f"{node}({result[node]})" for node in nodes]
    for u, v in zip(nodes, nodes[1:]):
        g.add_edge(u, v)
    pos = {node : (0, i) for i, node in enumerate(nodes)}
    nx.draw(g, pos, with_labels = True,
            width = 1.5, edge_color = 'red',
            node_size = 800, node_color = 'lightgreen',
            font_size = 12, font_family = 'cursive',
            edgecolors = 'black', linewidths = 1.5,
            margins = 0.2, clip_on = False)
    plt.suptitle("House Allocation(Constraint Satisfaction Problem)")
    plt.show()
    plt.clf()

#______________________________________________

def main():
    graph = {"A" : {"B":9,"C":4,"D":7},
             "B" : {"A":9,"E":11},
             "C" : {"A":4,"E":17,"F":12},
             "D" : {"A":7,"F":14},
             "E" : {"B":11,"G":5,"C":17},
             "F" : {"D":14,"C":12,"G":9},
             "G" : {"E":5,"F":9}}
    heuristic = {"A":21,"B":14,"C":18,"D":18,"E":5,"F":8,"G":0}
    pretty_print(graph, title = "Graph", weighted = True, directed = True, heuristic = heuristic)
    display(graph)
    
    BFS(graph, "A", "F")
    
    DFS(graph, "A", "F")
    
    UCS(graph, "A", "G")
    
    DLS(graph, "A", "G", 3)
    
    IDS(graph, "A", "G")
    
    AStar(graph, "A", "G", heuristic)
    
    IDAStar(graph, "A", "G", heuristic)
    
    #graph, heuristic, bound, source, goal = get_input(heuristic = True,weighted = True,bound = True)
    SMAStar(graph, "A", "G", heuristic, bound = 3)
    
    print("Genetic Algorithm Example 1(5 Queen): ")
    genetic(1000, ["32152","24345"])
    print()
    print("Genetic Algorithm Example 2(8 Queen): ")
    genetic(1000, ["57142860","56782463"])
    print()
    
    initsol = [300.0, 400.0]
    inittemp = 1000.0
    alpha = 0.95
    iters = 500
    bestsol, cost = simulated_annealing(initsol, inittemp, alpha, iters)
    print("Simulated Annealing Best Solution:",bestsol)
    print("Simulated Annealing Best Cost:",cost)
    print()
    
    board =[[5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]]
    sudoku_simulated_annealing(board)
    
    graph = {
        'A' : ['B', 'C'],
        'B' : ['D', 'E'],
        'C' : ['F', 'G'],
        'D' : ['H', 'I'],
        'E' : [10, 5],
        'F' : ['J', 'K'],
        'G' : ['L', 'M'],
        'H' : [11, 12],
        'I' : [8, 9],
        'J' : [8, 5],
        'K' : [12, 11],
        'L' : [12, 9],
        'M' : [8, 7],}
    show_tree(graph)
    print(graph)
    start = 'A'
    
    val, pruned, path = alphabeta(start, graph, True)#True means first node is max
    path = show_path(start, graph, path, val)
    print("Alpha Beta Pruning(Maximize):", val, " Pruned Branches:", ', '.join(pruned), " Path:",'->'.join(path))
    
    val, pruned, path = alphabeta(start, graph, False)#False means first node is min
    path = show_path(start, graph, path, val)
    print("Alpha Beta Pruning(Minimize):", val, " Pruned Branches:", ', '.join(pruned), " Path:",'->'.join(path))
    print()

    graph = {
        'A' : ['B', 'C'],
        'B' : ['A', 'C', 'D', 'E'],
        'C' : ['B', 'E'],
        'D' : ['A', 'B', 'E'],
        'E' : ['B', 'C', 'D']}
    
    colors = ["red","green","blue"]
    sol = backtrack_map(graph, colors)
    print("Constraint Satisfaction Problem(Map Coloring)")
    if sol:
        display_map(graph, sol.values())
        for (node, color) in sol.items():
            print("Node:",node," Color:",color)
    else:
        print("No Solution Exists")
    print()

    #Info: "There are 4 family namely A, B, C, D there are 4 houses namely 1,2,3,4"
    #1. C lives in a house higher than D
    #2. D lives next to A in Lower number House
    #3. There is at least one house between D and B
    #4. C doesn't live in house number 3
    #5. B doesn't live in house number 1
    locs = [1,2,3,4]
    houses = ['A','B','C','D']
    sol = backtrack_house(houses, locs)
    print("Constraint Satisfaction Problem(House Allocation)")
    if sol:
        display_house(sol)
        for node in sol:
            print("House:",node," Location:",sol[node])
    else:
        print("No Solution Exists")
main()
"""
bfs = """
import networkx as nx
import matplotlib.pyplot as plt

def display(graph, directed = False):
    g = nx.DiGraph(graph) if directed else nx.Graph(graph)
    nx.draw(g, with_labels = True)
    plt.suptitle("Breadth First Search")
    plt.show()
    plt.clf()
def print_path(node, parent):
    if node != None:
        return print_path(parent[node], parent) + [node]
    return []
def BFS(graph, start, goal):
    queue = [start]
    visited = []
    parent = {start : None}
    while queue:
        node = queue.pop(0)#First element
        visited.append(node)
        if node == goal:
            print(f"Result(BFS {start} to {goal}):",print_path(node, parent))
            return True 
        for adj in graph[node]:
            if adj not in visited and adj not in queue:
                queue.append(adj)
                parent[adj] = node
    print(f"Result(BFS {start} to {goal}): No Solution")
    return False
def get_graph(directed = False):
    graph = {}
    print("Enter Node Adjacency Pair")
    print("[PRESS ENTER TO STOP]")
    x = input()
    while x:
        x = x.split(maxsplit = 1)
        u, adj = x[0], {v.strip() for v in x[1].strip(' []').split(',') if v}
        graph[u] = graph.get(u,set()) | adj
        for v in adj:
            graph[v] = graph.get(v,set()) | ({u} if not directed else set())
        x = input()
    return graph
def example():
    graph = {"A" : ["B","C","D"],
             "B" : ["A","E"],
             "C" : ["A","E","F"],
             "D" : ["A","F"],
             "E" : ["B","G","C"],
             "F" : ["D","C","G"],
             "G" : ["E","F"]}
    display(graph)
    print(graph)
    BFS(graph, "A", "F")
    
def main():
    #example();return #Uncomment to run the example
    graph = get_graph(directed = False)#undirected graph
    source, goal = input("Enter source and goal: ").split()
    display(graph, directed = False)
    print(graph)
    BFS(graph, source, goal)
    
    #Sample output (Square brackets [] are optional)
    #Enter Node Adjacency Pair
    #[Press Enter To Stop]
    #A [B,C,D]
    #B [A,E]
    #C [A,E,F]
    #D [A,F]
    #E [B,G,C]
    #F [D,C,G]
    #G [E,F]

    #Enter source and goal: A F
    #Result(BFS A to F): ['A', 'C', 'F']
main()
"""
dfs = """
import networkx as nx
import matplotlib.pyplot as plt
def display(graph, directed = False):
    g = nx.DiGraph(graph) if directed else nx.Graph(graph)
    nx.draw(g, with_labels = True)
    plt.suptitle("Depth First Search")
    plt.show()
    plt.clf()
def print_path(node, parent):
    if node != None:
        return print_path(parent[node], parent) + [node]
    return []
def DFS(graph, start, goal):
    stack = [start]
    visited = []
    parent = {start : None}
    while stack:
        node = stack.pop()#last element
        visited.append(node)
        if node == goal:
            print(f"Result(DFS {start} to {goal}):",print_path(node, parent))
            return True
        for adj in graph[node]:
            if adj not in visited and adj not in stack:
                stack.append(adj)
                parent[adj] = node
    print(f"Result(DFS {start} to {goal}): No Solution")
    return False
def get_graph(directed = False):
    graph = {}
    print("Enter Node Adjacency Pair")
    print("[PRESS ENTER TO STOP]")
    x = input()
    while x:
        x = x.split(maxsplit = 1)
        u, adj = x[0], {v.strip() for v in x[1].strip(' []').split(',') if v}
        graph[u] = graph.get(u,set()) | adj
        for v in adj:
            graph[v] = graph.get(v,set()) | ({u} if not directed else set())
        x = input()
    return graph
def example():
    graph = {"A" : ["B","C","D"],
             "B" : ["A","E"],
             "C" : ["A","E","F"],
             "D" : ["A","F"],
             "E" : ["B","G","C"],
             "F" : ["D","C","G"],
             "G" : ["E","F"]}
    display(graph)
    print(graph)
    DFS(graph, "A", "F")

def main():
    #example();return #Uncomment to run the example
    graph = get_graph(directed = False)#undirected graph
    source, goal = input("Enter source and goal: ").split()
    display(graph, directed = False)
    print(graph)
    DFS(graph, source, goal)

    #Sample output (Square brackets [] are optional)
    #Enter Node Adjacency Pair
    #[Press Enter To Stop]
    #A [B,C,D]
    #B [A,E]
    #C [A,E,F]
    #D [A,F]
    #E [B,G,C]
    #F [D,C,G]
    #G [E,F]

    #Enter source and goal: A F
    #Result(DFS A to F): ['A', 'C', 'F']
main()
"""
ucs = """
import networkx as nx
import matplotlib.pyplot as plt
def display(graph, directed = False):
    graph = {u : {v : {'weight' : graph[u][v]} for v in graph[u]} for u in graph}
    g = nx.from_dict_of_dicts(graph)
    pos = nx.circular_layout(g)
    nx.draw(g, pos, with_labels = True)
    nx.draw_networkx_edge_labels(g, pos, edge_labels = nx.get_edge_attributes(g, 'weight'))
    plt.suptitle("Uniform Cost Search")
    plt.show()
    plt.clf()
def print_path(node, parent):
    if node != None:
        return print_path(parent[node], parent) + [node]
    return []
def UCS(graph, start, goal):
    queue = [start]
    visited = []
    parent = {start : None}
    cost = {start : 0}
    while queue:
        queue.sort(key = lambda x : cost[x])
        node = queue.pop(0)
        visited.append(node)
        if node == goal:
            print(f"Result(UCS {start} to {goal}):",print_path(node, parent),"Path cost =",cost[node])
            return True
        for adj in graph[node]:
            if adj not in visited:
                new_cost = cost[node] + graph[node][adj]
                if adj not in queue:
                    queue.append(adj)
                elif new_cost > cost[adj]:
                    continue
                cost[adj] = new_cost
                parent[adj] = node
    print(f"Result(UCS {start} to {goal}): No Solution")
    return False
def get_graph(directed = False):
    graph = {}
    print("Enter Node Adjacency Pair")
    print("[PRESS ENTER TO STOP]")
    x = input()
    while x:
        x = x.split(maxsplit = 1)
        u, adj = x[0], [v.strip(' ()') for v in x[1].strip('[]').split(',') if v] 
        adj = {v : int(w) for v, w in zip(adj[::2],adj[1::2])}
        graph[u] = graph.get(u, {}) | adj
        for v, w in adj.items():
            graph[v] = graph.get(v, {}) | ({u : w} if not directed else {})
        x = input()
    return graph
def example():
    graph = {"A" : {"B":9,"C":4,"D":7},
             "B" : {"A":9,"E":11},
             "C" : {"A":4,"E":17,"F":12},
             "D" : {"A":7,"F":14},
             "E" : {"B":11,"G":5,"C":17},
             "F" : {"D":14,"C":12,"G":9},
             "G" : {"E":5,"F":9}}
    display(graph)
    print(graph)
    UCS(graph, "A", "G")

def main():
    #example();return #Uncomment to run the example
    graph = get_graph(directed = False)#undirected graph
    source, goal = input("Enter source and goal: ").split()
    display(graph, directed = False)
    print(graph)
    UCS(graph, source, goal)

    #Sample output (Square brackets [] are optional)
    #Enter Node Adjacency Pair
    #[Press Enter To Stop]
    #A [(B,9),(C,4),(D,7)]
    #B [(E,11)]
    #C [(E,17),(F,12)]
    #D [(F,14)]
    #E [(G,5)]
    #F [(G,9)]
 
    #Enter source and goal:  A G
    #Result(UCS A to G): ['A', 'B', 'E', 'G'] Path cost = 25
main()
"""
dls = """
import networkx as nx
import matplotlib.pyplot as plt
def display(graph, directed = False):
    g = nx.DiGraph(graph) if directed else nx.Graph(graph)
    nx.draw(g, with_labels = True)
    plt.suptitle("Depth Limited Search")
    plt.show()
    plt.clf()
def print_path(node, parent):
    if node != None:
        return print_path(parent[node], parent) + [node]
    return []
def DLS(graph, start, goal, limit):
    result = recursive_dls(graph, start, goal, limit, [start])
    print(f"Result(DLS {start} to {goal}):",result,"at depth limit =",limit)
def recursive_dls(graph, node, goal, limit, visited):
    if node == goal:
        return [node]
    elif limit == 0:
        return 'cutoff'
    else:
        status = 'failure'
        for adj in graph[node]:
            if adj not in visited:
                visited.append(adj)
                result = recursive_dls(graph, adj, goal, limit - 1, visited)
                if result == 'cutoff':
                    status = 'cutoff'
                    visited.remove(adj)
                elif result != 'failure':
                    return [node] + result
        return status
def get_graph(directed = False):
    graph = {}
    print("Enter Node Adjacency Pair")
    print("[PRESS ENTER TO STOP]")
    x = input()
    while x:
        x = x.split(maxsplit = 1)
        u, adj = x[0], {v.strip() for v in x[1].strip(' []').split(',') if v}
        graph[u] = graph.get(u,set()) | adj
        for v in adj:
            graph[v] = graph.get(v,set()) | ({u} if not directed else set())
        x = input()
    return graph
def example():
    graph = {"A" : ["B","C","D"],
             "B" : ["A","E"],
             "C" : ["A","E","F"],
             "D" : ["A","F"],
             "E" : ["B","G","C"],
             "F" : ["D","C","G"],
             "G" : ["E","F"]}
    display(graph)
    print(graph)
    DLS(graph, "A", "F", 3)

def main():
    #example();return #Uncomment to run the example
    graph = get_graph(directed = False)#undirected graph
    source, goal, limit = input("Enter source, goal and depthlimit: ").split() 
    display(graph, directed = False)
    print(graph)
    DLS(graph, source, goal, int(limit))

    #Sample output (Square brackets [] are optional)
    #Enter Node Adjacency Pair
    #[Press Enter To Stop]
    #A [B,C,D]
    #B [A,E]
    #C [A,E,F]
    #D [A,F]
    #E [B,G,C]
    #F [D,C,G]
    #G [E,F]

    #Enter source, goal and depthlimit:  A G 3
    #Result(DLS A to G): ['A', 'D', 'F', 'G'] at depth limit = 3
main()
"""
ids = """
import networkx as nx
import matplotlib.pyplot as plt
def display(graph, directed = False):
    g = nx.DiGraph(graph) if directed else nx.Graph(graph)
    nx.draw(g, with_labels = True)
    plt.suptitle("Iterative Deepening Depth First Search")
    plt.show()
    plt.clf()
def print_path(node, parent):
    if node != None:
        return print_path(parent[node], parent) + [node]
    return []
def IDS(graph, start, goal):
    depth = 0
    while True:
        result = recursive_dls(graph, start, goal, depth, [start])
        print(f"Result(IDS/IDDFS {start} to {goal}):",result,"at depth limit =",depth)
        if result != 'cutoff':
            return
        depth += 1
def recursive_dls(graph, node, goal, limit, visited):
    if node == goal:
        return [node]
    elif limit == 0:
        return 'cutoff'
    else:
        status = 'failure'
        for adj in graph[node]:
            if adj not in visited:
                visited.append(adj)
                result = recursive_dls(graph, adj, goal, limit - 1, visited)
                if result == 'cutoff':
                    status = 'cutoff'
                    visited.remove(adj)
                elif result != 'failure':
                    return [node] + result
        return status
def get_graph(directed = False):
    graph = {}
    print("Enter Node Adjacency Pair")
    print("[PRESS ENTER TO STOP]")
    x = input()
    while x:
        x = x.split(maxsplit = 1)
        u, adj = x[0], {v.strip() for v in x[1].strip(' []').split(',') if v}
        graph[u] = graph.get(u,set()) | adj
        for v in adj:
            graph[v] = graph.get(v,set()) | ({u} if not directed else set())
        x = input()
    return graph
def example():
    graph = {"A" : ["B","C","D"],
             "B" : ["A","E"],
             "C" : ["A","E","F"],
             "D" : ["A","F"],
             "E" : ["B","G","C"],
             "F" : ["D","C","G"],
             "G" : ["E","F"]}
    display(graph)
    print(graph)
    IDS(graph, "A", "F")

def main():
    #example();return #Uncomment to run the example
    graph = get_graph(directed = False)#undirected graph
    source, goal = input("Enter source, goal: ").split() 
    display(graph, directed = False)
    print(graph)
    IDS(graph, source, goal)

    #Sample output (Square brackets [] are optional)
    #Enter Node Adjacency Pair
    #[PRESS ENTER TO STOP]
    #A [B,C,D]
    #B [A,E]
    #C [A,E,F]
    #D [A,F]
    #E [B,G,C]
    #F [D,C,G]
    #G [E,F]
 
    #Enter source, goal:  A G
    #Result(IDS/IDDFS): cutoff at depth limit = 0
    #Result(IDS/IDDFS): cutoff at depth limit = 1
    #Result(IDS/IDDFS): cutoff at depth limit = 2
    #Result(IDS/IDDFS): ['A', 'C', 'E', 'G'] at depth limit = 3
main()
"""
astar = """
import networkx as nx
import matplotlib.pyplot as plt
def display(graph, h, directed = False):
    graph = {u+" "+str(h[u]) : {v+" "+str(h[v]) : {'weight' : graph[u][v]} for v in graph[u]} for u in graph}
    g = nx.from_dict_of_dicts(graph)
    pos = nx.circular_layout(g)
    nx.draw(g, pos, with_labels = True)
    nx.draw_networkx_edge_labels(g, pos, edge_labels = nx.get_edge_attributes(g, 'weight'))
    plt.suptitle("AStar Search")
    plt.show()
    plt.clf()
def print_path(node, parent):
    if node != None:
        return print_path(parent[node], parent) + [node]
    return []
def AStar(graph, start, goal, h):
    queue = [start]
    visited = []
    parent = {start : None}
    g = {start : 0}
    f = {start : h[start]}
    while queue:
        queue.sort(key = lambda x : f[x])
        node = queue.pop(0)
        visited.append(node)
        if node == goal:
            print(f"Result(AStar {start} to {goal}):",print_path(node, parent),"Path cost =",g[node])
            return True
        for adj in graph[node]:
            if adj not in visited:
                gcost = g[node] + graph[node][adj]
                fcost = gcost + h[adj]
                if adj not in queue:
                    queue.append(adj)
                elif fcost > f[adj]:
                    continue
                g[adj] = gcost
                f[adj] = fcost
                parent[adj] = node
    print(f"Result(AStar {start} to {goal}): No Solution")
    return False
def get_graph(directed = False):
    graph = {}
    heuristic = {}
    print("Enter Node Adjacency Pair")
    print("[PRESS ENTER TO STOP]")
    x = input()
    while x:
        x = x.split(maxsplit = 2)
        u, heuristic[u] = x[0], int(x[1])
        adj = [v.strip(' ()') for v in x[2].strip('[]').split(',') if v] if len(x) == 3 else [] 
        adj = {v : int(w) for v, w in zip(adj[::2],adj[1::2])}
        graph[u] = graph.get(u, {}) | adj
        for v, w in adj.items():
            graph[v] = graph.get(v, {}) | ({u : w} if not directed else {})
        x = input()
    return graph, heuristic
def example():
    graph = {"A" : {"B":9,"C":4,"D":7},
             "B" : {"A":9,"E":11},
             "C" : {"A":4,"E":17,"F":12},
             "D" : {"A":7,"F":14},
             "E" : {"B":11,"G":5,"C":17},
             "F" : {"D":14,"C":12,"G":9},
             "G" : {"E":5,"F":9}}
    heuristic = {"A":21,"B":14,"C":18,"D":18,"E":5,"F":8,"G":0}
    print("Heuristic: ",heuristic)
    print(graph)
    display(graph, heuristic)
    AStar(graph, "A", "G", heuristic)

def main():
    #example();return #Uncomment to run the example
    graph, h = get_graph(directed = False)#undirected graph
    source, goal = input("Enter source and goal: ").split()
    display(graph, h, directed = False)
    print("Heuristic: ",h)
    print(graph)
    AStar(graph, source, goal, h)

    #Sample output (Square brackets [] are optional)
    #Enter Node Adjacency Pair
    #PRESS ENTER TO STOP]
    #A 21 [(B,9),(C,4),(D,7)]
    #B 14 [(E,11)]
    #C 18 [(E,17),(F,12)]
    #D 18 [(F,14)]
    #E 5 [(G,5)]
    #F 8 [(G,9)]
    #G 0 []
 
    #Enter source and goal:  A G
    #Result(AStar A to G): ['A', 'B', 'E', 'G'] Path cost = 25
main()
"""
idastar = """
import networkx as nx
import matplotlib.pyplot as plt
def display(graph, h, directed = False):
    graph = {u+" "+str(h[u]) : {v+" "+str(h[v]) : {'weight' : graph[u][v]} for v in graph[u]} for u in graph}
    g = nx.from_dict_of_dicts(graph)
    pos = nx.circular_layout(g)
    nx.draw(g, pos, with_labels = True)
    nx.draw_networkx_edge_labels(g, pos, edge_labels = nx.get_edge_attributes(g, 'weight'))
    plt.suptitle("IDAStar Search")
    plt.show()
    plt.clf()
def print_path(node, parent):
    if node != None:
        return print_path(parent[node], parent) + [node]
    return []
INF = float('inf')
def IDAStar(graph, start, goal, h):    
    parent = {start : None}    
    th = h[start]
    while True:
        result, new_th = recursive_dfs(graph, parent, start, goal, 0, h, th)
        if result is not None:
            result = print_path(result, parent)
            cost = sum([graph[n1][n2] for n1, n2 in zip(result,result[1:])])
            print(f"Result(IDAStar {start} to {goal}):",result,"Path cost =",cost)
            return
        elif new_th == INF:
            print(f"Result(IDAStar {start} to {goal}): failure")
            return
        th = new_th
def recursive_dfs(graph, parent, node, goal, g, h, th):
    f = g + h[node]
    if f > th:
        return None, f
    if node == goal:
        return node, f
    min_th = INF
    for adj in graph[node]:
        result, temp_th = recursive_dfs(graph, parent, adj, goal, g + graph[node][adj], h, th)
        if result is not None:
            parent[adj] = node
            return result, temp_th
        elif temp_th < min_th:
            min_th = temp_th
    return None, min_th
def get_graph(directed = False):
    graph = {}
    heuristic = {}
    print("Enter Node Adjacency Pair")
    print("[PRESS ENTER TO STOP]")
    x = input()
    while x:
        x = x.split(maxsplit = 2)
        u, heuristic[u] = x[0], int(x[1])
        adj = [v.strip(' ()') for v in x[2].strip('[]').split(',') if v] if len(x) == 3 else [] 
        adj = {v : int(w) for v, w in zip(adj[::2],adj[1::2])}
        graph[u] = graph.get(u, {}) | adj
        for v, w in adj.items():
            graph[v] = graph.get(v, {}) | ({u : w} if not directed else {})
        x = input()
    return graph, heuristic
def example():
    graph = {"A" : {"B":9,"C":4,"D":7},
             "B" : {"A":9,"E":11},
             "C" : {"A":4,"E":17,"F":12},
             "D" : {"A":7,"F":14},
             "E" : {"B":11,"G":5,"C":17},
             "F" : {"D":14,"C":12,"G":9},
             "G" : {"E":5,"F":9}}
    heuristic = {"A":21,"B":14,"C":18,"D":18,"E":5,"F":8,"G":0}
    print("Heuristic: ",heuristic)
    print(graph)
    display(graph, heuristic)
    IDAStar(graph, "A", "G", heuristic)

def main():
    #example();return #Uncomment to run the example
    graph, h = get_graph(directed = False)#undirected graph
    source, goal = input("Enter source and goal: ").split()
    display(graph, h, directed = False)
    print("Heuristic: ",h)
    print(graph)
    IDAStar(graph, source, goal, h)

    #Sample output (Square brackets [] are optional)
    #Enter Node Adjacency Pair
    #PRESS ENTER TO STOP]
    #A 21 [(B,9),(C,4),(D,7)]
    #B 14 [(E,11)]
    #C 18 [(E,17),(F,12)]
    #D 18 [(F,14)]
    #E 5 [(G,5)]
    #F 8 [(G,9)]
    #G 0 []
 
    #Enter source and goal:  A G
    #Result(IDAStar A to G): ['A', 'B', 'E', 'G'] Path cost = 25
main()
"""
smastar = """
import networkx as nx
import matplotlib.pyplot as plt
def display(graph, h, directed = False):
    graph = {u+" "+str(h[u]) : {v+" "+str(h[v]) : {'weight' : graph[u][v]} for v in graph[u]} for u in graph}
    g = nx.from_dict_of_dicts(graph)
    pos = nx.circular_layout(g)
    nx.draw(g, pos, with_labels = True)
    nx.draw_networkx_edge_labels(g, pos, edge_labels = nx.get_edge_attributes(g, 'weight'))
    plt.suptitle("SMAStar Search")
    plt.show()
    plt.clf()
def print_path(node, parent):
    if node != None:
        return print_path(parent[node], parent) + [node]
    return []
def SMAStar(graph, start, goal, h, bound):
    queue = [start]
    visited = []
    parent = {start : None}
    g = {start : 0}
    f = {start : h[start]}
    backup = {}
    while queue:
        queue.sort(key = lambda x : f[x])
        node = queue.pop(0)
        visited.append(node)
        if node == goal:
            print(f"Result(SMAStar {start} to {goal}):",print_path(node, parent),"Path cost =",g[node],"Bound =",bound)
            return True
        successors = []
        for adj in graph[node]:
            if adj in visited:
                continue
            gcost = g[node] + graph[node][adj]
            fcost = gcost + h[adj]
            if adj in queue:
                if fcost >= f[adj]:
                    continue
            elif len(queue) < bound:
                    queue.append(adj)
            else:
                worst = max(queue, key = lambda x : f[x])
                if fcost < f[worst]:
                    backup[worst] = f[worst]
                    queue.remove(worst)
                    queue.append(adj)
                else:
                    continue
            g[adj] = gcost
            f[adj] = fcost
            parent[adj] = node
            successors.append(adj)
        if not successors and node in backup:
            f[node] = backup[node]
        elif not successors:
            f[node] = float('inf')
    print(f"Result(SMAStar {start} to {goal}): No Solution Bound = ",bound)
    return False
def get_graph(directed = False):
    graph = {}
    heuristic = {}
    print("Enter Node Adjacency Pair")
    print("[PRESS ENTER TO STOP]")
    x = input()
    while x:
        x = x.split(maxsplit = 2)
        u, heuristic[u] = x[0], int(x[1])
        adj = [v.strip(' ()') for v in x[2].strip('[]').split(',') if v] if len(x) == 3 else [] 
        adj = {v : int(w) for v, w in zip(adj[::2],adj[1::2])}
        graph[u] = graph.get(u, {}) | adj
        for v, w in adj.items():
            graph[v] = graph.get(v, {}) | ({u : w} if not directed else {})
        x = input()
    return graph, heuristic
def example():
    graph = {"A" : {"B":9,"C":4,"D":7},
             "B" : {"A":9,"E":11},
             "C" : {"A":4,"E":17,"F":12},
             "D" : {"A":7,"F":14},
             "E" : {"B":11,"G":5,"C":17},
             "F" : {"D":14,"C":12,"G":9},
             "G" : {"E":5,"F":9}}
    heuristic = {"A":21,"B":14,"C":18,"D":18,"E":5,"F":8,"G":0}
    print("Heuristic: ",heuristic)
    print(graph)
    display(graph, heuristic)
    SMAStar(graph, "A", "G", heuristic, 4)

def main():
    #example();return #Uncomment to run the example
    graph, h = get_graph(directed = False)#undirected graph
    source, goal, bound = input("Enter source and goal and bound: ").split()
    display(graph, h, directed = False)
    print("Heuristic: ",h)
    print(graph)
    SMAStar(graph, source, goal, h, int(bound))

    #Sample output (Square brackets [] are optional)
    #Enter Node Adjacency Pair
    #PRESS ENTER TO STOP]
    #A 21 [(B,9),(C,4),(D,7)]
    #B 14 [(E,11)]
    #C 18 [(E,17),(F,12)]
    #D 18 [(F,14)]
    #E 5 [(G,5)]
    #F 8 [(G,9)]
    #G 0 []
 
    #Enter source and goal and bound:  A G 4
    #Result(SMAStar A to G): ['A', 'C', 'F', 'G'] Path cost = 25 Bound = 4
main()
"""
genetic = """
from random import randint as rint
n = 8
def show(b):
    board = [['_'] * n for _ in range(n)]
    for i in range(n):
        board[int(b[i])-1][i] = 'Q'
    print(f" {' '.join(['_']*n)}")
    for i in board:
        print(f"|{'|'.join(i)}|")
def mutate(b1, b2):
    b1, b2 = list(b1), list(b2)
    x, y = rint(0,n-1), rint(0,n-1)
    b1[x], b2[x] = b2[x], b1[x]
    b1[y] = str(int(y) + 1)
    return (''.join(b1),''.join(b2))
def crossover(b1, b2):
    b1, b2 = list(b1), list(b2)
    x = rint(1,n-1)
    b1[0:x], b2[0:x] = b2[0:x], b1[0:x]
    return (''.join(b1), ''.join(b2))
def fitness(b):
    b = list(b)
    attacks = 0
    for i in range(n):
        for j in range(i+1, n):
            if b[i] == b[j] or abs(int(b[i]) - int(b[j])) == j - i:
                attacks += 1
    return attacks
def genetic(gen, pop):
    global n 
    n = len(pop[0])
    pq = pop
    for i in range(1,gen+1):
        pq.sort(key = lambda x : fitness(x))
        b1 = pq.pop(0)
        b2 = pq.pop(0)
        pq.clear()
        if fitness(b1) == 0:
            print("Goal State:",b1,"Generation:",i)
            show(b1)
            return
        x1, x2 = crossover(b1, b2)
        x3, x4 = crossover(b2, b1)
        pq = [x1, x2, x3, x4, *mutate(x1, x2), *mutate(x2, x1), b1, b2]
    print("Most Evolved State:",pq[0],"Generation:",i,"Attacks:",fitness(pq[0]))
    show(pq[0])

def main():
    #no of queens is inferred in genetic()
    print("Genetic Algorithm Example 1(5 Queen): ")
    genetic(1000, ["32152","24345"])
    print()
    print("Genetic Algorithm Example 2(8 Queen): ")
    genetic(1000, ["57142860","56782463"])

    #Sample output
    #Genetic Algorithm Example 1(5 Queen): 
    #Most Evolved State: 14352 Generation: 1000 Attacks: 2
    #Genetic Algorithm Example 2(8 Queen): 
    #Goal State: 57142863 Generation: 1
main()
"""
sa = """
import math
import random
def simulated_annealing(initsol, inittemp, alpha, iters):
    currsol = initsol
    cost = fcost(currsol)
    sol = currsol
    mincost = cost
    temp = inittemp
    for iteration in range(iters):
        neighbor = successors(currsol)
        ncost = fcost(neighbor)
        costdiff = ncost - cost
        if costdiff < 0 or random.random() < math.exp(-costdiff/temp):
            currsol = neighbor
            cost = ncost
            if cost < mincost:
                sol = currsol
                mincost = cost
        temp *= alpha
    return sol, mincost
def fcost(sol):
    return sum([i**2 for i in sol])
def successors(sol, step = 1.0):
    succ = [x + random.uniform(-step,step) for x in sol]
    return succ

def main():
    initsol = [300.0, 400.0]
    inittemp = 1000.0
    alpha = 0.95
    iters = 500
    
    bestsol, cost = simulated_annealing(initsol, inittemp, alpha, iters)
    print("Best Solution:",bestsol)
    print("Best Cost:",cost)

    #Sample input/output (can change due to the use of random)
    #Best Solution: [225.56303970871514, 294.69364950481685]
    #Best Cost: 137723.03194110325
main()
"""
sudoku = """
import math 
import random
def display(board):
    for row in board:
        print(' '.join(str(num) if num != 0 else '.' for num in row))
    print()
def fill(board):
    for i in range(9):
        choices = list(set(range(1,10)) - set(board[i]) - {0})
        random.shuffle(choices)
        for j in range(9):
            if board[i][j] == 0:
                board[i][j] = choices.pop()
def cost(board):
    conflicts = 0
    for n in range(9):
        row = board[n]
        col = [x[n] for x in board]
        conflicts += len(row) - len(set(row))
        conflicts += len(col) - len(set(col))
    for l in [0,3,6]:
        for k in [0,3,6]:
            block = []
            for i in range(0+l,3+l):
                for j in range(0+k,3+k):
                    block.append(board[i][j])
            conflicts += 9 - len(set(block))
    return conflicts
def next(board, fixed):
    neighbor = [[x for x in row] for row in board]
    i = random.randint(0,8)
    cols = [j for j in range(9) if (i,j) not in fixed]
    if len(cols) >= 2:
        j1, j2 = random.sample(cols, 2)
        neighbor[i][j1], neighbor[i][j2] = neighbor[i][j2], neighbor[i][j1]
    return neighbor
def simulated_annealing(board, initial_temp = 1.0, cooling_rate = 0.99, min_temp = 0.001):
    fixed = [(x,y) for x in range(9) for y in range(9) if board[x][y] != 0]
    fill(board)
    current = best = board
    temp = initial_temp
    while temp > min_temp:
        neighbor = next(current,fixed)
        delta = cost(neighbor) - cost(current)
        if delta < 0:
            current = neighbor
            if cost(neighbor) < cost(best):
                best = neighbor
        else:
            if random.random() < math.exp(-delta/temp):
                current = neighbor
        temp *= cooling_rate
    print(f"Sudoku ({'Best Possible State | Attacks = '+str(cost(best)) if cost(best) else 'Solved'})") 
    display(best)

def main():
    board =[[5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]]
    simulated_annealing(board)                                       
main()
"""
alphabeta = """
import networkx as nx
import matplotlib.pyplot as plt
def show_tree(graph):
    graph = {node : [adj for adj in graph[node]] for node in graph}
    terminal_nodes = set()
    for node in graph:
        for i in range(len(graph[node])):
            x = str(graph[node][i])
            if x.isdigit():
                while x in terminal_nodes:
                    x+=" "
                graph[node][i] = x
                terminal_nodes.add(x)
    g = nx.DiGraph(graph)
    levels = nx.single_source_shortest_path_length(g, next(iter(g.nodes)))
    layers = {}
    for node, level in levels.items():
        layers[level] = layers.get(level, []) + [node]
    pos = {}
    for level, nodes in layers.items():
        x_offset = (len(nodes) - 1)/2
        for i, node in enumerate(nodes):
            x = i - x_offset
            y = -level
            pos[node] = (x,y)
    plt.figure(figsize = (8,4))
    nx.draw(g, pos, with_labels = True, 
            node_size = 600, node_color = 'lightgreen',
            font_size = 12, font_family = 'cursive',
            arrows = False, width = 1.5, edge_color = 'red',
            edgecolors = 'black', linewidths = 1.5,
            margins = 0.1, clip_on = False)
    plt.suptitle("Alpha Beta Pruning")
    plt.show()
    plt.clf()
MIN = -float('inf')
MAX = float('inf')
def alphabeta(node, graph, ismax, pruned = [], alpha = MIN, beta = MAX, path = {}):
    if str(node).isdigit():
        return int(node), pruned, path
    option = MIN if ismax else MAX
    for child in graph[node]:
        val, _, _ = alphabeta(child, graph, not ismax, pruned, alpha, beta, path)
        if ismax:
            option = max(option, val)
            alpha = max(option, alpha)
            path[node] = alpha
        else:
            option = min(option, val)
            beta = min(option, beta)
            path[node] = beta
        if alpha >= beta:
            i = graph[node].index(child)+1
            pruned += [f"{node}-{adj}" for adj in graph[node][i:]]
            break
    return option, pruned, path
def show_path(node, graph, path, value):
    for adj in graph[node]:
        if str(adj).isdigit():
            return [node,str(value)]
        if path[adj] == value:
            return [node] + show_path(adj, graph, path, value)
            
def main():
    graph = {
        'A' : ['B', 'C'],
        'B' : ['D', 'E'],
        'C' : ['F', 'G'],
        'D' : ['H', 'I'],
        'E' : [10, 5],
        'F' : ['J', 'K'],
        'G' : ['L', 'M'],
        'H' : [11, 12],
        'I' : [8, 9],
        'J' : [8, 5],
        'K' : [12, 11],
        'L' : [12, 9],
        'M' : [8, 7]}

    show_tree(graph)
    print(graph)
    start = 'A'
    
    val, pruned, path = alphabeta(start, graph, True)#True means first node is max
    path = show_path(start, graph, path, val)
    print("Alpha Beta Pruning(Maximize):", val, " Pruned Branches:", ', '.join(pruned), " Path:",'->'.join(path))
    
    val, pruned, path = alphabeta(start, graph, False)#False means first node is min
    path = show_path(start, graph, path, val)
    print("Alpha Beta Pruning(Minimize):", val, " Pruned Branches:", ', '.join(pruned), " Path:",'->'.join(path))
    print()
    
    #Sample input/output    
    #Alpha Beta Pruning(Maximize): 10  Pruned Branches: I-9, J-5, M-7  Path: A->B->E->10
    #Alpha Beta Pruning(Minimize): 8  Pruned Branches: I-9, J-5, M-7, K-11, L-9  Path: A->C->F->J->8
main()
"""
csp_map = """
import networkx as nx
import matplotlib.pyplot as plt
def backtrack(graph, colors):
    assign = {node : -1 for node in graph}
    return rec_backtrack(assign, graph, colors)
def rec_backtrack(assign, graph, colors):
    if -1 not in assign.values():
        return assign
    node = [x for x in assign if assign[x] == -1][0]
    for color in colors:
        if all(assign[adj] != color for adj in graph[node]):
            assign[node] = color
            result = rec_backtrack(assign, graph, colors)
            if result:
                return result
            assign[node] = -1
    return None
def display_map(graph, colors = None):
    g = nx.DiGraph(graph)
    #nx.draw_circular(g, with_labels = True, node_color = colors)
    nx.draw_circular(g, with_labels = True,
                    node_size = 600, node_color = colors,
                    font_size = 12, font_family = 'cursive',
                    arrows = False, width = 1.25,
                    edgecolors = 'black', linewidths = 1.5,
                    margins = 0.375, clip_on = False)
    plt.suptitle("Map Coloring(Constraint Satisfaction Problem)")
    plt.show()
    plt.clf()

def main():
    graph = {
        'A' : ['B', 'C'],
        'B' : ['A', 'C', 'D', 'E'],
        'C' : ['B', 'E'],
        'D' : ['A', 'B', 'E'],
        'E' : ['B', 'C', 'D']}
    
    colors = ["red","green","blue"]
    sol = backtrack(graph, colors)
    
    if sol:
        display_map(graph, sol.values())
        for (node, color) in sol.items():
            print("Node:",node," Color:",color)
    else:
        print("No Solution Exists")
    
    #Sample Input/Output
    #Node:  A  Color: red
    #Node:  B  Color: green
    #Node:  C  Color: blue
    #Node:  D  Color: blue
    #Node:  E  Color: red
main()
"""
csp_house = """
import networkx as nx
import matplotlib.pyplot as plt
def check(assign, loc):
    #constraints given in the question
    #change it accordinly

    a = assign['A']
    b = assign['B']
    c = assign['C']
    d = assign['D']
    
    #1. C lives in a house higher than D
    if c != -1 and d != -1 and c < d:return False

    #2. D lives next to A in Lower number House
    if d != -1 and a != -1 and (a - d) != 1:return False

    #3. There is at least one house between D and B    
    if d != -1 and b != -1 and abs(d - b) == 1:return False

    #4. C doesn't live in house number 3
    if c != -1 and c == 3:return False

    #5. B doesn't live in house number 1
    if b != -1 and b == 1:return False
        
    if loc in assign.values():
        return False
    return True
def backtrack(houses, locs):
    assign = {house : -1 for house in houses}    
    return rec_backtrack(assign, locs)
def rec_backtrack(assign, locs):
    if check(assign, -1):
        return assign
    choices = [x for x in assign if assign[x] == -1]
    house = choices[0] if choices else None
    for loc in locs:
        if check(assign, loc):
            assign[house] = loc
            res = rec_backtrack(assign, locs)
            if res:
                return res
            assign[house] = -1
    return None
def display_house(result):
    g = nx.Graph()
    nodes = list(result.keys())
    nodes.sort(key = lambda x : result[x])
    nodes = [f"{node}({result[node]})" for node in nodes]
    for u, v in zip(nodes, nodes[1:]):
        g.add_edge(u, v)
    pos = {node : (0, i) for i, node in enumerate(nodes)}
    nx.draw(g, pos, with_labels = True,
            width = 1.5, edge_color = 'red',
            node_size = 800, node_color = 'lightgreen',
            font_size = 12, font_family = 'cursive',
            edgecolors = 'black', linewidths = 1.5,
            margins = 0.2, clip_on = False)
    plt.suptitle("House Allocation(Constraint Satisfaction Problem)")
    plt.show()
    plt.clf()

def main():
    #Info: "There are 4 family namely A, B, C, D there are 4 houses namely 1,2,3,4"
    #1. C lives in a house higher than D
    #2. D lives next to A in Lower number House
    #3. There is at least one house between D and B
    #4. C doesn't live in house number 3
    #5. B doesn't live in house number 1
    locs = [1,2,3,4]
    houses = ['A','B','C','D']
    sol = backtrack(houses, locs)
    if sol:
        display_house(sol)
        for node in sol:
            print("House:",node," Location:",sol[node])
    else:
        print("No Solution Exists")

    #Sample Input/Output
    #House: A  Location: 2
    #House: B  Location: 3
    #House: C  Location: 4
    #House: D  Location: 1
main()
"""

chat = """
/*
How to run
==========
save the file as chat.java (filename can be anything)
Command Prompt 1 (go to the location the file is saved)
javac *.java
java Server

Command Prompt 2 (go to the location the file is saved)
java Client
*/

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.net.*;

class Client extends JFrame{
    JTextField jt;
    JButton send;
    JLabel lbl;
    public static void main(String[] args) {
	new Client();
    }
    Client(){
        setTitle("Client");
	setSize(400, 200);
        setVisible(true);
	setLayout(new FlowLayout());
	lbl = new JLabel("Enter a string:");
        jt = new JTextField(20);
        send = new JButton("Send");
	add(lbl);
	add(jt);
	add(send);
	validate();
        send.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ae) {
                try{
                    Socket s = new Socket("localhost", 1234);
                    DataOutputStream out = new DataOutputStream(s.getOutputStream());
                    out.writeUTF(jt.getText());
		    jt.setText("");
                    s.close();
                }catch(Exception e){System.out.println(e);}
            }
        });
    }
}

class Server extends JFrame{
    JTextArea jta;
    String newline = System.lineSeparator();
    public static void main(String[] args) {
	new Server();
    }
    Server(){
        setTitle("Server");
        setSize(400, 200);
        setVisible(true);
        jta = new JTextArea("Waiting for message..."+newline);
        add(jta);
	validate();
	try{
		ServerSocket ss = new ServerSocket(1234);
		while(true){
			Socket s = ss.accept();
	                DataInputStream in = new DataInputStream(s.getInputStream());
               		String msg = in.readUTF();
		        jta.append("Received: "+msg+" ("+check(msg)+")"+newline);
               		s.close();
                }
	}catch(Exception e){System.out.println(e);}
    }
    String check(String msg){
	StringBuffer rmsg = new StringBuffer(msg);
	rmsg.reverse();
	return msg.equalsIgnoreCase(new String(rmsg)) ? "It is a palindrome" : "It is not a palindrome";
    }
}
"""
file_transfer = """
/*
How to run
==========
save the file as filetransfer.java (filename can be anything)
Command Prompt 1 (go to the location the file is saved)
javac *.java
java Server

Command Prompt 2 (go to the location the file is saved)
java Client

select file_to_send.txt which will be there in the file location
(any file can be sent)
*/

import java.io.*;
import java.net.*;
import javax.swing.*;
import java.awt.event.*;

class Client extends JFrame {
	JTextArea jta;
	JButton send;
	JFileChooser jc;
	static String newline = System.lineSeparator();
	Client(){
		setTitle("File Client");
		setSize(400, 300);
		setVisible(true);
		jta = new JTextArea();
		send = new JButton("Send File");
		jc = new JFileChooser();
		send.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e){
				int op = jc.showOpenDialog(null);
				if(op == JFileChooser.APPROVE_OPTION)
					sendFile(jc.getSelectedFile());
			}
		});
		add(new JScrollPane(jta), "Center");
		add(send, "South");
		validate();
	}
	void sendFile(File f) {
		try{
			Socket s = new Socket("localhost", 5000);
			jta.setText("Connected to server"+newline);
			FileInputStream fin = new FileInputStream(f);
			OutputStream out = s.getOutputStream();

			byte[] buffer = new byte[1024];
			int bytesRead;
			while ((bytesRead = fin.read(buffer)) != -1){
				for (int i = 0; i < bytesRead; i++){
					byte plainByte = buffer[i];
					byte cipherByte = (byte) ((plainByte + 3) % 256);
					jta.append("Plain Text: " + plainByte + " (" + (char) plainByte + ") -> Cipher Text: " + cipherByte + " (" + (char) cipherByte + ")"+newline);
					buffer[i] = cipherByte;
				}
				out.write(buffer, 0, bytesRead);
			}
			fin.close();
			out.close();
			s.close();
			jta.append("File encrypted and sent successfully"+newline);
		}catch(Exception e){System.out.println(e);}
	}
	public static void main(String[] args){
		try{
			FileWriter fout = new FileWriter("file_to_send.txt");
			fout.write("Hello World"+newline+"Hello To JAVA");
			fout.close();
			new Client();
		}catch(Exception e){System.out.println(e);}
	}
}

class Server extends JFrame{
	JTextArea jta;
	String newline = System.lineSeparator();
	Server(){
		setTitle("File Server");
		setSize(400, 300);
		setVisible(true);
        	jta = new JTextArea();
        	add(new JScrollPane(jta));
		validate();
        	try{
            		ServerSocket ss = new ServerSocket(5000);
            		jta.append("Server is listening on port 5000"+newline);
	    		for(int n=1;n<=10;n++){
            			Socket s = ss.accept();
            			jta.setText("Client connected"+newline);
            			InputStream in = s.getInputStream();
            			FileOutputStream fout = new FileOutputStream("received_file_"+n+".txt");

            			byte[] buffer = new byte[1024];
            			int bytesRead;
            			while ((bytesRead = in.read(buffer)) != -1){
                			for (int i = 0; i < bytesRead; i++){
                    				byte cipherByte = buffer[i];
                    				byte plainByte = (byte) ((cipherByte - 3 + 256) % 256);
                    				jta.append("Cipher Text: " + cipherByte + " (" + (char) cipherByte + ") -> Plain Text: " + plainByte + " (" + (char) plainByte + ")"+newline);
                    				buffer[i] = plainByte;
                			}
                			fout.write(buffer, 0, bytesRead);
            			}
            			fout.close();
	            		in.close();
        	    		s.close();
	            		jta.append("File received and decrypted successfully"+newline);
			}
			ss.close();
        	}catch(Exception e){System.out.println(e);}
	}
	public static void main(String[] args){
		new Server();
	}
}
"""
rmi = """
/*
How to run
==========
save the file as rmi.java (filename can be anything)
Command Prompt 1 (go to the location the file is saved)
javac *.java
start rmiregistry
java Server

Command Prompt 2 (go to the location the file is saved)
java Client localhost

Note: If version error occurs, Compile following way:
javac --release 8 *.java
*/

import java.net.*;
import java.rmi.*;
import java.rmi.server.*;

interface MyServerIntf extends Remote{	
	String add(double a, double b) throws RemoteException;
}

class MyServerImpl extends UnicastRemoteObject implements MyServerIntf{
	MyServerImpl()throws RemoteException{}
	public String add(double a, double b)throws RemoteException{
		return a+" + "+b+" = "+(a+b);
	}	
}

class Client{
	public static void main(String[] arg){
		try{
			String name;
			if(arg.length == 0)
				name = "rmi://localhost/RMServer";
			else
				name = "rmi://"+arg[0]+"/RMServer";
			MyServerIntf asif = (MyServerIntf)Naming.lookup(name);
			System.out.println("Addition: "+asif.add(1200,1300));
		}catch(Exception e){System.out.println("Exception: "+e);}
	}
}


class Server{
	public static void main(String[] arg){
		try 	{
			MyServerImpl asi = new MyServerImpl();
			Naming.rebind("RMServer",asi);
			System.out.println("Server Started...");
		}
		catch(Exception e){System.out.println("Exception: "+e);}
	}
}
"""
wired_tcl = """
#How to run
#==========
#save this file as wired.tcl in desktop folder
#also save wired.awk file in the same location
#open desktop right-click and choose 'Open in Terminal'
#run this command
#ns wired.tcl

#both nam and awk file will be executed automatically

#create a simulator object 
set ns [new Simulator]

#create a trace file, this file is for logging purpose 
set tracefile [open wired.tr w]
$ns trace-all $tracefile

#create a animation infomration or NAM file creation
set namfile [open wired.nam w]
$ns namtrace-all $namfile

#create nodes
set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]

#creation of link between nodes with DropTail Queue
#Droptail means Dropping the tail.
$ns duplex-link $n0 $n1 5Mb 2ms DropTail
$ns duplex-link $n2 $n1 10Mb 5ms DropTail
$ns duplex-link $n1 $n4 3Mb 10ms DropTail
$ns duplex-link $n4 $n3 100Mb 2ms DropTail
$ns duplex-link $n4 $n5 4Mb 10ms DropTail

#creation of Agents
#node 0 to Node 3
set udp [new Agent/UDP]
set null [new Agent/Null]
$ns attach-agent $n0 $udp
$ns attach-agent $n3 $null
$ns connect $udp $null

#creation of TCP Agent
set tcp [new Agent/TCP]
set sink [new Agent/TCPSink]
$ns attach-agent $n2 $tcp
$ns attach-agent $n5 $sink
$ns connect $tcp $sink

#creation of Application CBR, FTP
#CBR - Constant Bit Rate (Example nmp3 files that have a CBR or 192kbps, 320kbps, etc.)
#FTP - File Transfer Protocol (Ex: To download a file from a network)
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp

set ftp [new Application/FTP]
$ftp attach-agent $tcp

#Start the traffic 
$ns at 1.0 "$cbr start"
$ns at 2.0 "$ftp start"

$ns at 10.0 "finish"

#the following procedure will be called at 10.0 seconds 
proc finish {} {
 global ns tracefile namfile
 $ns flush-trace
 close $tracefile
 close $namfile
 puts "Executing nam file"
 exec nam wired.nam &
 exec awk -f wired.awk wired.tr &
 exit 0
}

puts "Simulation is starting..."
$ns run
"""
wired_awk = """
BEGIN{
	r1=r2=d1=d2=total=0
	ratio=tp1=tp2=0.0
}

{
	if($1 =="r" && $4 == 3 && $5=="cbr")r1++
	if($1 =="d" && $4 == 3 && $5=="cbr")d1++
	if($1 =="r" && $4 == 5 && $5=="tcp")r2++
	if($1 =="d" && $4 == 5 && $5=="tcp")d2++
}

END{
	total = r1+r2+d1+d2
	ratio = (r1+r2)*100/total
	tp1 = (r1+d1)*8/1000000
	tp2 = (r2+d2)*8/1000000
	print("")
	print("Wired-Network")
	print("Packets Received:",r1+r2)
	print("Packets Dropped :",d1+d2)
	print("Packets Delivery Ratio:",ratio,"%")
	print("UDP Throughput:",tp1,"Mbps")
	print("TCP Throughput:",tp2,"Mbps")
}
"""
wireless_tcl = """
#How to run
#==========
#save this file as wireless.tcl in desktop folder
#also save wireless.awk file in the same location
#open desktop right-click and choose 'Open in Terminal'
#run this command
#ns wireless.tcl

#both nam and awk file will be executed automatically


#Example of Wireless networks
#Step 1 initialize variables
#Step 2 - Create a Simulator object
#step 3 - Create Tracing and animation file
#step 4 - topography
#step 5 - GOD - General Operations Director
#step 6 - Create nodes
#Step 7 - Create Channel (Communication PATH)
#step 8 - Position of the nodes (Wireless nodes needs a location)
#step 9 - Any mobility codes (if the nodes are moving)
#step 10 - TCP, UDP Traffic
#run the simulation

#initialize the variables
set val(chan)           Channel/WirelessChannel    ;#Channel Type
set val(prop)           Propagation/TwoRayGround   ;# radio-propagation model
set val(netif)          Phy/WirelessPhy            ;# network interface type WAVELAN DSSS 2.4GHz
set val(mac)            Mac/802_11                 ;# MAC type
set val(ifq)            Queue/DropTail/PriQueue    ;# interface queue type
set val(ll)             LL                         ;# link layer type
set val(ant)            Antenna/OmniAntenna        ;# antenna model
set val(ifqlen)         50                         ;# max packet in ifq
set val(nn)             6                          ;# number of mobilenodes
set val(rp)             AODV                       ;# routing protocol
set val(x)  500   ;# in metres
set val(y)  500   ;# in metres
#Adhoc OnDemand Distance Vector

#creation of Simulator
set ns [new Simulator]

#creation of Trace and namfile 
set tracefile [open wireless.tr w]
$ns trace-all $tracefile

#Creation of Network Animation file
set namfile [open wireless.nam w]
$ns namtrace-all-wireless $namfile $val(x) $val(y)

#create topography
set topo [new Topography]
$topo load_flatgrid $val(x) $val(y)

#GOD Creation - General Operations Director
create-god $val(nn)

set channel1 [new $val(chan)]
set channel2 [new $val(chan)]
set channel3 [new $val(chan)]

#configure the node
$ns node-config -adhocRouting $val(rp) \
  -llType $val(ll) \
  -macType $val(mac) \
  -ifqType $val(ifq) \
  -ifqLen $val(ifqlen) \
  -antType $val(ant) \
  -propType $val(prop) \
  -phyType $val(netif) \
  -topoInstance $topo \
  -agentTrace ON \
  -macTrace ON \
  -routerTrace ON \
  -movementTrace ON \
  -channel $channel1 

set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]

$n0 random-motion 0
$n1 random-motion 0
$n2 random-motion 0
$n3 random-motion 0
$n4 random-motion 0
$n5 random-motion 0

$ns initial_node_pos $n0 20
$ns initial_node_pos $n1 20
$ns initial_node_pos $n2 20
$ns initial_node_pos $n3 20
$ns initial_node_pos $n4 20
$ns initial_node_pos $n5 50

#initial coordinates of the nodes 
$n0 set X_ 10.0
$n0 set Y_ 20.0
$n0 set Z_ 0.0

$n1 set X_ 210.0
$n1 set Y_ 230.0
$n1 set Z_ 0.0

$n2 set X_ 100.0
$n2 set Y_ 200.0
$n2 set Z_ 0.0

$n3 set X_ 150.0
$n3 set Y_ 230.0
$n3 set Z_ 0.0

$n4 set X_ 430.0
$n4 set Y_ 320.0
$n4 set Z_ 0.0

$n5 set X_ 270.0
$n5 set Y_ 120.0
$n5 set Z_ 0.0
#Dont mention any values above than 500 because in this example, we use X and Y as 500,500

#mobility of the nodes
#At what Time? Which node? Where to? at What Speed?
$ns at 1.0 "$n1 setdest 490.0 340.0 25.0"
$ns at 1.0 "$n4 setdest 300.0 130.0 5.0"
$ns at 1.0 "$n5 setdest 190.0 440.0 15.0"
#the nodes can move any number of times at any location during the simulation (runtime)
$ns at 20.0 "$n5 setdest 100.0 200.0 30.0"

#creation of agents
set tcp [new Agent/TCP]
set sink [new Agent/TCPSink]
$ns attach-agent $n0 $tcp
$ns attach-agent $n5 $sink
$ns connect $tcp $sink
set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ns at 1.0 "$ftp start"

set udp [new Agent/UDP]
set null [new Agent/Null]
$ns attach-agent $n2 $udp
$ns attach-agent $n3 $null
$ns connect $udp $null
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$ns at 1.0 "$cbr start"

$ns at 30.0 "finish"

proc finish {} {
 global ns tracefile namfile
 $ns flush-trace
 close $tracefile
 close $namfile
 puts "Executing nam file"
 exec nam wireless.nam &
 exec awk -f wireless.awk wireless.tr &
 exit 0
}

puts "Starting Simulation"
$ns run
"""
wireless_awk = """
BEGIN {
	rec=sen=drp=0
	res=start=end=0.0
}

{
	if($1 == "s")sen++
	if($1 == "r"){
		if(rec==0)start = $2
		rec++		
		res += $8
		end = $2
	}
	if($1 == "D")drp++
}

END {
	print("")
	print("Wireless-Network")
	print("Number Of Packets Sent : ", sen)
	print("Number Of Packets Recieved : ", rec)
	print("Number Of Packets Dropped  : ", drp)
	print("Start Of Simulation (in sec) : ", start)
	print("End Of Simulation (in sec)   : ", end)
	print("Total Throughput : ",((res*8) / ((end-start)*1000000))," Mbps")
	print("Packet Delivery Ratio: ",rec*100/sen,"%")
}
"""

def display(name = ""):
    available = {'AI & DS             ' : "Lab",
                 '0   |  all          ' : "All",
                 '1   |  bfs          ' : "Breadth First Search",
                 '2   |  dfs          ' : "Depth First Search",
                 '3   |  ucs          ' : "Uniform Cost Search",
                 '4   |  dls          ' : "Depth Limited Search", 
                 '5   |  ids          ' : "Iterative Deepening Search(IDDFS)", 
                 '6   |  astar        ' : "A*", 
                 '7   |  idastar      ' : "Iterative Deepening A*", 
                 '8   |  smastar      ' : "Simplified Memory Bounded A*",
                 '9   |  genetic      ' : "Genetic Algorithm", 
                 '10  |  sa           ' : "Simulated Annealing",
                 '11  |  sudoku       ' : "Solving Sudoku(Simulated Annealing)",
                 '12  |  alphabeta    ' : "Alpha-Beta Pruning",
                 '13  |  map          ' : "Map Coloring(Constraint Satisfaction Problem)",
                 '14  |  house        ' : "House Allocation(Constraint Satisfaction Problem)",
                 '                    ' : "",
                 'Computer Networks   ' : "Lab",
                 '15  |  chat         ' : "Chat Application",
                 '16  |  ft           ' : "File Transfer",
                 '17  |  rmi          ' : "RMI(Remote Method Invocation)",
                 '18  |  wired.tcl    ' : "Wired Network TCL Script",
                 '19  |  wired.awk    ' : "Wired Network AWK File",
                 '20  |  wireless.tcl ' : "Wireless Network TCL Script",
                 '21  |  wireless.awk ' : "Wireless Network AWK File",
                 }
    try:
        if isinstance(name,str):
            name = name.lower()
        if   name in ["bfs", 1]             :   print(bfs)
        elif name in ["dfs", 2]             :   print(dfs)
        elif name in ["ucs", 3]             :   print(ucs)
        elif name in ["dls", 4]             :   print(dls)
        elif name in ["ids", 5]             :   print(ids)
        elif name in ["astar", 6]           :   print(astar)
        elif name in ["idastar", 7]         :   print(idastar)
        elif name in ["smastar", 8]         :   print(smastar)
        elif name in ["genetic", 9]         :   print(genetic)
        elif name in ["sa", 10]             :   print(sa)
        elif name in ["sudoku", 11]         :   print(sudoku)
        elif name in ["alphabeta", 12]      :   print(alphabeta)
        elif name in ["map", 13]            :   print(csp_map)
        elif name in ["house", 14]          :   print(csp_house)
        elif name in ["chat", 15]           :   print(chat)
        elif name in ["ft", 16]             :   print(file_transfer)
        elif name in ["rmi", 17]            :   print(rmi)
        elif name in ["wired.tcl", 18]      :   print(wired_tcl)
        elif name in ["wired.awk", 19]      :   print(wired_awk)
        elif name in ["wireless.tcl", 20]   :   print(wireless_tcl)
        elif name in ["wireless.awk", 21]   :   print(wireless_awk)
        elif name in ["", "all", 0]         :   print(code)
        else:
            print("Invalid Value! Refer Below Table")
            for k, v in available.items():
                print(k,v,sep = " : ")
    except:
        pass

sudoku_lb = """
import math 
import random
from tqdm import tqdm

def display(board):
    for row in board:
        print(' '.join(str(num) if num != 0 else '.' for num in row))
    print()
def fill(board):
    for i in range(9):
        choices = list(set(range(1,10)) - set(board[i]) - {0})
        random.shuffle(choices)
        for j in range(9):
            if board[i][j] == 0:
                board[i][j] = choices.pop()
def cost(board):
    conflicts = 0
    for n in range(9):
        row = board[n]
        col = [x[n] for x in board]
        conflicts += len(row) - len(set(row))
        conflicts += len(col) - len(set(col))
    for l in [0,3,6]:
        for k in [0,3,6]:
            block = []
            for i in range(0+l,3+l):
                for j in range(0+k,3+k):
                    block.append(board[i][j])
            conflicts += 9 - len(set(block))
    return conflicts
def next(board, fixed):
    neighbor = [[x for x in row] for row in board]
    i = random.randint(0,8)
    cols = [j for j in range(9) if (i,j) not in fixed]
    if len(cols) >= 2:
        j1, j2 = random.sample(cols, 2)
        neighbor[i][j1], neighbor[i][j2] = neighbor[i][j2], neighbor[i][j1]
    return neighbor
def simulated_annealing(board, initial_temp = 1.0, cooling_rate = 0.99, min_temp = 0.001):
    board = [[x for x in row] for row in board]
    fixed = [(x,y) for x in range(9) for y in range(9) if board[x][y] != 0]
    fill(board)
    current = best = board
    temp = initial_temp
    while temp > min_temp:
        neighbor = next(current,fixed)
        delta = cost(neighbor) - cost(current)
        if delta < 0:
            current = neighbor
            if cost(neighbor) < cost(best):
                best = neighbor
        else:
            if random.random() < math.exp(-delta/temp):
                current = neighbor
        temp *= cooling_rate
    return best


board =[[5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]]

best = simulated_annealing(board)
for i in tqdm (range (1000), desc="Solving "):
    if cost(best) == 0:continue
    result = simulated_annealing(board)
    if cost(result) < cost(best):
        best = result
print(f"Sudoku ({'Best Possible State | Attacks = '+str(cost(best)) if cost(best) else 'Solved'})") 
display(best)
"""

def ghost(key = None, what = ""):
    if key and isinstance(key,str) and key == "r690z4t13x":
        available = {'101  or  sudoku   ' : "Solving Sudoku(Loading Bar)"}
        try:
            if isinstance(what,str):
                what =  what.lower()
            if what in ["sudoku", 101]   :   print(sudoku_lb)
            else:
                print("Invalid Value! Refer Below Table")
                for k, v in available.items():
                    print(k,v,sep = " : ")
        except:
            pass