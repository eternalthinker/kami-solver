# kami-solver
Solution finder for [KAMI 2](https://itunes.apple.com/us/app/kami-2/id1133161444?mt=8) game on IOS (or [KAMI](https://play.google.com/store/apps/details?id=air.com.stateofplaygames.kamifree&hl=en) on Android). 
Uses DFS (naive) or A* search (much much faster) to reach a solution.

The puzzle is entered as separate regions, each with a unique id and information on color and adjacent regions.

For example, the puzzle below is divided into separate regions identified by letters:   

<img src="https://github.com/eternalthinker/kami-solver/blob/master/kami-2-puzzle-examples/kami1_regions.jpg" width="200px"/>  

The above puzzle is represented as follows:
```python
colors = ["ORANGE", "BLUE", "CREAM"]
# Region (id, color_index, adjacent_region_ids)
A = Region("A", 2, {'B', 'D', 'E'})
B = Region("B", 0, {'A', 'D', 'C'})
C = Region("C", 2, {'B', 'D', 'E'})
D = Region("D", 1, {'A', 'B', 'C', 'E'})
E = Region("E", 0, {'D', 'A', 'C'})
```
The solution is computed as follows:

```python
kami = Kami([A, B, C, D, E], colors)
kami.solve(2) # Solve within a maximum of 2 moves
```
```
Solution found:
        Begin
        Move 2: set D to ORANGE
        Move 1: set B+E+D to CREAM
Finished in 0.01346732 seconds
```

There is also a `solve_i()` method which attempts the puzzle without any knowledge of the optimal number of moves.
It uses iterative deepening while calling the above `solve(n)` method:  
```python
kami = Kami([A, B, C, D, E], colors)
kami.solve_i() # Finds solution and minimal number of moves required
```

Following is an example involving more regions. As the number of steps increase, the solver could run for a few seconds due to the size of the puzzle:

<img src="https://github.com/eternalthinker/kami-solver/blob/master/kami-2-puzzle-examples/kami3_regions.jpg" width="250px"/>

```python
# See source for complete puzzle representation
kami = Kami([A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X], colors)
kami.solve(5)
```
```
Solution found!
        Begin
        Move 5: set R to CREAM
        Move 4: set Q+S+R+L to RED
        Move 3: set P+K+Q+S+R+L to BLACK
        Move 2: set C+E+I+M+P+K+Q+S+R+L+U+T to CREAM
        Move 1: set B+D+F+H+J+O+N+C+E+I+M+P+K+Q+S+R+L+U+T+W+V to BLACK
Finished in 0.36057810783 seconds
```
