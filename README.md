# kami-solver
Solution finder for [KAMI 2](https://itunes.apple.com/us/app/kami-2/id1133161444?mt=8) game on IOS (or [KAMI](https://play.google.com/store/apps/details?id=air.com.stateofplaygames.kamifree&hl=en) on Android). 
Uses DFS or Greedy search (slightly faster) to reach a solution.

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
```

Following is an example involving more regions. This could run for a while due size of the puzzle:

<img src="https://github.com/eternalthinker/kami-solver/blob/master/kami-2-puzzle-examples/kami3_regions.jpg" width="250px"/> 
