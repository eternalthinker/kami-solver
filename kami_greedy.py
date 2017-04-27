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
        
    def set_color(self, color, regions, regions_map, color_counts):
        #map_str = ", ".join([("%s:%s" % (key, regions_map[key].adj)) for key in regions_map])
        #print "Setting color of %s to %s with map-{%s}, regions-%s" % (self.name, color, map_str, regions)
        if self.color == color:
            return
        merged_regions = set()
        new_adj = set()
        for a_region_name in self.adj:
            a_region = regions_map[a_region_name]
            if a_region.color == color:
                a_region.adj.remove(self.name)
                merged_regions.add(a_region_name)
                new_adj = new_adj.union(a_region.adj)
        # Merge any adj regions of same color
        if len(merged_regions) > 0:
            color_counts[self.color] -= 1
            color_counts[color] -= len(merged_regions)-1
            merged_regions.add(self.name)
            new_adj = new_adj.union(self.adj.difference(merged_regions))
            for m_region in merged_regions:
                regions.remove(m_region)
                regions_map.pop(m_region)
            new_region = Region("+".join(list(merged_regions)), color)
            new_region.adj = new_adj
            regions.append(new_region.name)
            regions_map[new_region.name] = new_region
            for adj_name in new_adj:
                adj_region = regions_map[adj_name]
                adj_region.adj = adj_region.adj.difference(merged_regions)
                adj_region.adj.add(new_region.name)
        else:
            color_counts[self.color] -= 1
            regions_map[self.name].color = color
        #map_str = ", ".join([("%s:%s" % (key, regions_map[key].adj)) for key in regions_map])
        #print "After color setting: map-{%s}, regions-%s" % (map_str, regions)
        

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
    def __init__(self, regions, regions_map, last_move="Begin"):
        self.last_move = last_move
        self.regions = regions
        self.regions_map = regions_map
            
    def __str__(self):
        return self.last_move    
           
           
class Kami:
    def __init__(self, regions_list, colors):
        # debug vars
        self.start_time = 0
        # end of debug vars
        self.colors = colors
        self.regions = []
        self.regions_map = {}
        self.color_counts = [0 for _ in colors]
        for region in regions_list:
            self.regions.append(region.name)
            self.regions_map[region.name] = region
            self.color_counts[region.color] += 1
            
    def solve(self, num_moves):
        self.start_time = time.time()
        first_node = KamiNode(self.regions, self.regions_map)
        paths = [ Path([first_node], len(self.regions), num_moves, self.color_counts) ]
        while len(paths) > 0:
            cur_path = heapq.heappop(paths)
            #print "Selected %s %s %s" % (cur_path.path, cur_path.num_regions, cur_path.moves_left)
            cur_node = cur_path.path[-1]
            cur_path.path[-1] = cur_node.last_move
            # num_nodes = 0
            cur_node.regions.sort() # Optimization: color regions with most adjacent regions first
            for region_name in cur_node.regions:
                region = cur_node.regions_map[region_name]
                for color in range(len(self.colors)):
                    if region.color == color:
                        continue
                    # num_nodes += 1
                    move = "Move %d: set %s to %s" % (cur_path.moves_left, region.name, self.colors[color])
                    # Deepcopy before region.set_color() call before set_color changes region info due to merging
                    regions_c = cur_node.regions[:]
                    color_counts_c = cur_path.color_counts[:]
                    regions_map_c = {}
                    for region_name_c in cur_node.regions_map:
                        region_c = cur_node.regions_map[region_name_c]
                        regions_map_c[region_name_c] = Region(region_c.name, region_c.color, set(list(region_c.adj)))
                    region.set_color(color, regions_c, regions_map_c, color_counts_c)
                    if len(regions_c) == 1:
                        print "Solution found!"
                        for move0 in cur_path.path:
                            print "\t", move0
                        print "\t", move
                        exec_time = time.time() - self.start_time
                        print "Finished in %s seconds" % exec_time
                        sys.exit(0) # Comment this to print all possible solutions
                    if cur_path.moves_left-1 <= 0:
                        #print "Out of moves. Pruning path"
                        continue
                    # Thanks <https://github.com/brownbytes> for this heuristic. 
                    # Hugely cuts down on run time! (45mins -> 9secs for large example)
                    num_uniq_colors = sum([1 for i in color_counts_c if i > 0])
                    if num_uniq_colors - (cur_path.moves_left-1) > 1:
                        #print "Certain failure. Pruning path"
                        continue
                    new_node = KamiNode(regions_c, regions_map_c, move)
                    new_path = Path(cur_path.path[:])
                    new_path.update(new_node, len(regions_c), cur_path.moves_left-1, color_counts_c)
                    heapq.heappush(paths, new_path)
            #print "==== Generated %d paths" % num_nodes
    
    def print_regions(self):
        for region in self.regions_map.values():
            print "%s:%s  " % (region.name, self.colors[region.color]),
        print ""
           
           
def main():

    # Runtime around 9 seconds    
    
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
    kami.solve(5)

    '''
    colors = ["RED", "BLACK", "CREAM"]
    A = Region("A", 0, {"B", "C"})
    B = Region("B", 1, {"A"})
    C = Region("C", 1, {"A"})
    kami = Kami([A, B, C], colors)
    kami.solve(1)
    '''
    
    '''
    colors = ["ORANGE", "BLUE", "CREAM"]
    A = Region("A", 2, {'B', 'D', 'E'})
    B = Region("B", 0, {'A', 'D', 'C'})
    C = Region("C", 2, {'B', 'D', 'E'})
    D = Region("D", 1, {'A', 'B', 'C', 'E'})
    E = Region("E", 0, {'D', 'A', 'C'})
    kami = Kami([A, B, C, D, E], colors)
    kami.solve(2) # Solve within a maximum of 2 moves
    '''
    
    '''
    colors = ["ORANGE", "BLUE", "CREAM", "BLACK"]
    A = Region("A", 2, {'B', 'E', 'F'})
    B = Region("B", 3, {'A', 'C', 'E'})
    C = Region("C", 0, {'B', 'E', 'D'})
    D = Region("D", 2, {'C', 'E', 'G'})
    E = Region("E", 1, {'A', 'B', 'C', 'D', 'F', 'G'})
    F = Region("F", 3, {'A', 'E', 'G'})
    G = Region("G", 0, {'F', 'E', 'D'})
    kami = Kami([A, B, C, D, E, F, G], colors)
    kami.solve(3)
    '''
    
if __name__ == "__main__":
    main()      
           
           
           
           
           
           
           
           
           
            
