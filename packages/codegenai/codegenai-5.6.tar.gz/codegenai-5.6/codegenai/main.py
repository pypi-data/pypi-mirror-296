from codegenai.aids import *
from codegenai.cn import *
from codegenai.special import *

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
            if name.isdigit():
                name = int(name)
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