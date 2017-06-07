#!/usr/bin/env python
#!/usr/bin/env python
#
# Author: Rahul Anand <et@eternalthinker.co>
# Description:
#   Solution finder for KAMI 2 game on IOS
#   Greedy logic based path finding 
#    - Prefers paths with minimum number of regions left
#    - Prunes paths where unique_colors_in_board - moves_left > 1
# ================================================================


import sys
import time
import heapq


class Region:
    def __init__(self, name, color, adj=set()):
        self.name = name
        self.color = color
        self.adj = adj

    def __cmp__(self, other):
        return (len(other.adj) - len(self.adj))

    def __str__(self):
        return "%s:%s" %(self.name, len(self.adj))
        

class Path:
    def __init__(self, path=[], num_regions=float('inf'), moves_left=0, color_counts=[]):
        self.path = path
        self.num_regions = num_regions
        self.moves_left = moves_left
        self.color_counts = color_counts
        
    def update(self, node, num_regions, moves_left, color_counts):
        self.path.append(node)
        self.num_regions = num_regions
        self.moves_left = moves_left
        self.color_counts = color_counts
        
    def __cmp__(self, other):
        return self.num_regions - other.num_regions
        
    def __str__(self):
        return "<regions:%d, path:%d>" % (self.num_regions, len(self.path))
        
        
class KamiNode:
    def __init__(self, regions_map, last_move="Begin"):
        self.last_move = last_move
        self.regions_map = regions_map
            
    def __str__(self):
        return self.last_move    
           
           
class Kami:
    def __init__(self, regions_list, colors):
        # debug vars
        # end of debug vars
        self.colors = colors
        self.regions_map = {}
        self.color_counts = [0 for _ in colors]
        for region in regions_list:
            self.regions_map[region[0]] = region
            self.color_counts[region[1]] += 1
            
    def solve(self, num_moves):
        start_time = time.time()
        first_node = KamiNode(self.regions_map)
        paths = [ Path([first_node], len(self.regions_map.keys()), num_moves, self.color_counts) ]
        while len(paths) > 0:
            cur_path = heapq.heappop(paths)
            #print "Selected %s %s %s" % (cur_path.path, cur_path.num_regions, cur_path.moves_left)
            cur_node = cur_path.path[-1]
            cur_path.path[-1] = cur_node.last_move
            # num_nodes = 0
            # Optimization: color regions with most adjacent regions first
            regions = list(cur_node.regions.keys())
            regions.sort(cmp = lambda x, y: len(y[2]) - len(x[2])) 
            for region_name in regions:
                region = cur_node.regions_map[region_name]
                for color in range(len(self.colors)):
                    if region[1] == color:
                        continue
                    # num_nodes += 1
                    move = "Move %d: set %s to %s" % (cur_path.moves_left, region[0], self.colors[color])
                    region, regions_map, color_counts = set_color(region, color, regions_map, color_counts)
                    if len(list(regions_map.keys())) == 1:
                        print "Solution found!"
                        for move0 in cur_path.path:
                            print "\t", move0
                        print "\t", move
                        exec_time = time.time() - start_time
                        print "Finished in %s seconds" % exec_time
                        return True # Comment this to print all possible solutions
                    if cur_path.moves_left-1 <= 0:
                        #print "Out of moves. Pruning path"
                        continue
                    # Thanks <https://github.com/brownbytes> for this heuristic. 
                    # Hugely cuts down on run time! (45mins -> 4secs for large example)
                    num_uniq_colors = sum([1 for i in color_counts_c if i > 0])
                    if num_uniq_colors - (cur_path.moves_left-1) > 1:
                        # print "Certain failure. Pruning path"
                        continue
                    new_node = KamiNode(regions_map_c, move)
                    new_path = Path(cur_path.path[:])
                    new_path.update(new_node, len(regions_c), cur_path.moves_left-1, color_counts_c)
                    heapq.heappush(paths, new_path)
            #print "==== Generated %d paths" % num_nodes
        return False

    def solve_i(self):
        start_time = time.time()
        is_solved = False
        depth = 0
        while not is_solved:
            depth += 1
            is_solved = self.solve(depth)
        exec_time = time.time() - start_time
        print "All iterations finished in %s seconds. Optimal move count: %s" % (exec_time, depth)
    
    def print_regions(self):
        for region in self.regions_map.values():
            print "%s:%s  " % (region.name, self.colors[region.color]),
        print ""
    

def set_color(region, color, regions_map, color_counts):
    if region[1] == color:
        return
    merged = False
    merged_regions = set()
    new_adj = set()
    for a_region_name in region[2]:
        a_region = regions_map[a_region_name]
        if a_region[1] == color:
            if not merged:
                merged = True
                regions_map_c = {}
                for k, t in regions_map.items():
                    regions_map_c[k] = [t[0], t[1], set(t[2])]
                regions_map = regions_map_c
            a_region[2].remove(region[0])
            merged_regions.add(a_region_name)
            new_adj = new_adj.union(a_region[2])
    color_counts = color_counts[:]
    if len(merged_regions) > 0:
         color_counts[region[1]] -= 1
         color_counts[color] -= len(merged_regions) - 1
         merged_regions.add(region[0])
         new_adj = new_adj.union(region[2].difference(merged_regions))
         for m_region in merged_regions:
            regions_map.pop(m_region)
            new_region = ["+".join(list(merged_regions)), color, new_adj]
            regions_map[new_region[0]] = new_region
            for adj_name in new_adj:
                adj_region = regions_map[adj_name]
                adj_region[2] = adj_region.adj.difference(merged_regions)
                adj_region[2].add(new_region.name)
    else:
        color_counts[region[1]] -= 1
        regions_map[region[0]][1] = color

    return regions_map, color_counts

           
def main():

    # Runtime around 4 seconds    
    
    '''
    colors = ["BLACK", "CREAM", "RED"]
    
    A = Region("A", 0, {'B', 'H'})
    B = Region("B", 1, {'A', 'C'})
    C = Region("C", 0, {'B', 'D', 'K', 'J'})
    D = Region("D", 1, {'C', 'K', 'E'})
    E = Region("E", 0, {'D', 'K', 'L', 'F'})
    F = Region("F", 1, {'E', 'G'})
    G = Region("G", 0, {'F', 'N'})
    H = Region("H", 1, {'A', 'I'})
    I = Region("I", 0, {'H', 'J', 'O', 'P'})
    J = Region("J", 1, {'C', 'I', 'P', 'K'})
    K = Region("K", 2, {'J', 'C', 'D', 'L', 'E'})
    L = Region("L", 1, {'K', 'E', 'M', 'R'})
    M = Region("M", 0, {'L', 'N', 'S', 'R'})
    N = Region("N", 1, {'G', 'M'})
    O = Region("O", 1, {'I', 'T', 'P'})
    P = Region("P", 2, {'O', 'I', 'J', 'Q', 'T'})
    Q = Region("Q", 1, {'P', 'T', 'R', 'U'})
    R = Region("R", 2, {'Q', 'L', 'M', 'S', 'U'})
    S = Region("S", 1, {'R', 'M', 'U'})
    T = Region("T", 0, {'O', 'P', 'Q', 'V'})
    U = Region("U", 0, {'Q', 'S', 'R', 'W'})
    V = Region("V", 1, {'T', 'X'})
    W = Region("W", 1, {'U', 'X'})
    X = Region("X", 0, {'V', 'W'})

    kami = Kami([A , B , C , D , E , F , G , H , I , J , K , L , M , N , O , P , Q , R , S , T , U , V , W , X], colors)
    print "Solving with the knowledge that optimal number of moves is 5:"
    kami.solve(5)
    print "\nSolving without knowledge of optimal number of moves:"
    kami.solve_i()
    '''

    colors = ["BLACK", "CREAM", "RED"]

    A = ["A", 0, {'B', 'H'}]
    B = ["B", 1, {'A', 'C'}]
    C = ["C", 0, {'B', 'D', 'K', 'J'}]
    D = ["D", 1, {'C', 'K', 'E'}]
    E = ["E", 0, {'D', 'K', 'L', 'F'}]
    F = ["F", 1, {'E', 'G'}]
    G = ["G", 0, {'F', 'N'}]
    H = ["H", 1, {'A', 'I'}]
    I = ["I", 0, {'H', 'J', 'O', 'P'}]
    J = ["J", 1, {'C', 'I', 'P', 'K'}]
    K = ["K", 2, {'J', 'C', 'D', 'L', 'E'}]
    L = ["L", 1, {'K', 'E', 'M', 'R'}]
    M = ["M", 0, {'L', 'N', 'S', 'R'}]
    N = ["N", 1, {'G', 'M'}]
    O = ["O", 1, {'I', 'T', 'P'}]
    P = ["P", 2, {'O', 'I', 'J', 'Q', 'T'}]
    Q = ["Q", 1, {'P', 'T', 'R', 'U'}]
    R = ["R", 2, {'Q', 'L', 'M', 'S', 'U'}]
    S = ["S", 1, {'R', 'M', 'U'}]
    T = ["T", 0, {'O', 'P', 'Q', 'V'}]
    U = ["U", 0, {'Q', 'S', 'R', 'W'}]
    V = ["V", 1, {'T', 'X'}]
    W = ["W", 1, {'U', 'X'}]
    X = ["X", 0, {'V', 'W'}]




if __name__ == "__main__":
    main()      
           
           
           
           
           
           
           
           
           
            
