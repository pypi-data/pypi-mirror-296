[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/LX4PRb-c)
# Instructions

In this homework you are asked to create a Python package that implements Dijkstra's shortest path algorithm among other algorithms. The name of the package must be **graphs_username**, where **username** should be replaced by your MSU Denver username. For example, my library was named **graphs_tmota**. 

The implementation for Dijkstra's algorithm is given to you as the goal of this homework is for you to practice packaging a code into a specific format. You should create a public GitHub repository for you project so others can contribute to it in the future. The repository should have a well-written README file and the main branch protected. There should be a dev branch as well. 

To get credit for this assignment you must change this README file and add the URL of your public GitHub repository below: 

```
URL for your GitHub repository: 
```

The expected structure for the GitHub repository is the following: 

```
src
|__graphs_<username>
   |__ __init__.py
   |__ heapq.py
   |__ sp.py
|__test.py
|__README.md
|__pyproject.toml
```

In addition, I should be able to install your Python package using pip3 and run the code below, replacing **tmota** with your username. 

```
from graphs_tmota import sp
import sys

if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        print(f'Use: {sys.argv[0]} graph_file')
        sys.exit(1)

    graph = {}
    with open(sys.argv[1], 'rt') as f:
        f.readline() # skip first line
        for line in f:
            line = line.strip()
            s, d, w = line.split()
            s = int(s)
            d = int(d)
            w = int(w)
            if s not in graph:
                graph[s] = {}
            graph[s][d] = w
    
    s = 0
    dist, path = sp.dijkstra(graph, s)
    print(f'Shortest distances from {s}:')
    print(dist)
    for d in path: 
        print(f'spf to {d}: {path[d]}')
```

# Rubric

```
+1 GitHub repository has main and dev branches, with the main branch protected
+1 the GitHub repository has a README file that explains what is this library about 
+3 the library can be installed using pip3 and it is usable 
+1 (bonus) other graph-related algorithm is added to the library
```

# The Shortest Path Problem

A graph is a data structure that connects nodes identified by labels. In a graph, a node is normally called **vertex** and the connections between two vertices is called **edge**. The cost to travel through an edge is its **weight**. Below is an example of a weighted graph with 9 vertices. 

![pic1.png](pics/pic1.png)

The **shortest path problem** is about finding the shortest paths from a given source vertex to all vertices. For example, the shortest path to reach vertex "1" from source vertex "0" is shown below, and it has a cost of 4. 

![pic2.png](pics/pic2.png)

The shortest path to reach vertex "8" from source vertex "0" is shown below, and it has a cost of 14. 

![pic3.png](pics/pic3.png)

# Dijkstra's Shortest Path Algorithm

Edsger W. Dijkstra was a Dutch computer scientist that made many contributions to the field, including a solution to the shortest path problem in a graph. The solution discussed here uses a min-heap to store the shortest known distances from the source. Let's look at a step-by-step execution of the algorithm for the example above. 

The algorithm begins by adding the cost to reach the source vertex, which is (of course) 0. We will use the notation (source, weight) to represent that. In the solution for the shortest path problem, the heap uses the weight of an edge to sort the values. A distance list is created to record the cost to reach each of the destinations from source. The distance list is initialized with the maximum possible value for the weight, represented as ∞, except to reach the source, which should be set to zero. 

The distances are initialized as: [0, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞]

Hint: to represent ∞ in your code use **sys.maxsize**. 

Next, the algorithm will run a loop until the heap becomes empty. At each iteration of that loop, the following steps are taken: 

* the top of the heap (i.e., its smaller element) is removed; 
* refer to that edge as (u, w), where w represents the best (known) cost to reach node u from source; 
* next, the algorithm evaluates if the cost to reach each of u's neighbors is better than what is known so far; 
* for example, if v is one of u's neighbor, then the algorithm checks if the cost to reach node u plus the weight from u to v is smaller than what is recorded in the distance array; 
* if that is the case, the distance array is updated; 
* also, if the cost is updated, the algorithm needs to update that cost if edge v is found in the heap. 

For the example, (u, w) = (0, 0) in the first iteration. Nodes 1 and 7 can be reached from u=0 with costs 4 and 8, respectively. Therefore, the distances are updated to [0, 4, ∞, ∞, ∞, ∞, ∞, 8, ∞]. Also, (1, 4) and (7, 8) are added to the heap, which should now look like: 

```
    (1, 4)
(7, 8)
```

On the second iteration, (u, w) = (1, 4).  Nodes 0, 2 and 7 can be reached from u=1 with costs 4, 8 and 11, respectively. The distance to node 2 is updated (with a cost of 4+8=12) and the pair (2, 12) is added to the heap. The distance to node 0 does not get updated because travelling to node 0 through node 1 didn't improve the cost: 4 vs. 0. Also, the distance to node 7 does not get updated because travelling to node 7 through node 1 didn't improve the cost: 15 vs. 8. The heap should now look like: 

```
    (7, 8)
(2, 12)    
```

The distances are now: [0, 4, 12, ∞, ∞, ∞, ∞, 8, -]

On the third iteration, (u, w) = (7, 8).  Nodes 0, 1, 6, and 8 can be reached from u=7 with costs 8, 11, 1 and 7, respectively. The distance to node 6 is updated (with a cost of 8+1=9) and the pair (6, 9) is added to the heap. The distance to node 8 is also updated (with a cost of 8+7=15) and the pair (8, 15) is added to the heap. The heap should now look like: 

```
    (6, 9)
(2, 12) (8, 15)  
```

The distances are now: [0, 4, 12, ∞, ∞, ∞, 9, 8, 15]

The algorithm repeats until the heap becomes empty. At the end of the loop the array of distances should have the lowest costs to reach each of the destinations from the source. 
