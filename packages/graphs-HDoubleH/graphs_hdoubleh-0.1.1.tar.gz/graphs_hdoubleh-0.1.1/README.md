# HDoubleH's Graphs Algorithm Library

This package implements two graph algorithms in python, including **Dijkstra's Shortest Path Algorithm** and **Tarjan's Algorithm for Strongly Connected Components**.

Graphs are data structures which connect nodes identified by labels. 

- **Dijkstra's Shortest Path Algorithm**: This computes the shortest path from a single source node to all the other nodes in a graph. It will find the shortest path from a single source node to all other nodes in a weighted graph with non-negative edge weights. It operates by iteratively expanding the node with the smallest known distance and updating the distances to its neighbors.

- **Tarjan's Algorithm for Strongly Connected Components**: This algorithm detects all the strongly connected components (SCCs) in a directed graph using a depth-first search. Each SCC is a maximal subgraph where every node is reachable from every other node in the same subgraph. 

# Usage

**Dijkstra's Shortest Path Algorithm**- python src/test.py graph.txt
**Tarjan's Algorithm for Strongly Connected Components**- python src/test_tarjan.py graph.txt

# Installation 
you can install this package with - pip3 install graphs_HDoubleH