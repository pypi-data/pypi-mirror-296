import sys
from graphs_HDoubleH import tarjan  # Import Tarjan's Algorithm

if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        print(f'Use: {sys.argv[0]} graph_file')
        sys.exit(1)

    # Load graph from the file
    graph = {}
    with open(sys.argv[1], 'rt') as f:
        f.readline()  # skip the first line
        for line in f:
            line = line.strip()
            s, d, w = line.split()
            s = int(s)
            d = int(d)
            w = int(w)
            if s not in graph:
                graph[s] = {}
            graph[s][d] = w

    # Run Tarjan's Algorithm to find SCCs
    sccs = tarjan.tarjan_scc(graph)
    
    # Output the results
    print(f'Strongly Connected Components (SCCs): {sccs}')