#!/usr/bin/env python
#
# Author: Rahul Anand <et@eternalthinker.co>
# Description:
#   Solution finder for KAMI 2 game on IOS
#   DFS based path finding
#
# ==================================================

import sys
import time

class Region:
    def __init__(self, name, color, adj=set()):
        self.name = name
        self.color = color
        self.adj = adj
        
    def set_color(self, color, regions, regions_map):
        map_str = ", ".join([("%s:%s" % (key, regions_map[key].adj)) for key in regions_map])
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
           regions_map[self.name].color = color
        map_str = ", ".join([("%s:%s" % (key, regions_map[key].adj)) for key in regions_map])
        #print "After color setting: map-{%s}, regions-%s" % (map_str, regions)
           
class Kami:
    def __init__(self, regions_list, colors):
        # debug vars
        self.start_time = 0
        # end of debug vars
        self.colors = colors
        self.regions = []
        self.regions_map = {}
        for region in regions_list:
            self.regions.append(region.name)
            self.regions_map[region.name] = region
            
    def solve(self, num_moves):
        self.print_regions()
        self.count = 0
        self.num_moves = num_moves
        self.start_time = time.time()
        self.solve_r(self.regions, self.regions_map, self.colors, num_moves, [])
            
    def solve_r(self, regions, regions_map, colors, moves_left, path):
        if len(regions) == 1:
            print "Solution found:"
            for move in path:
                print "\t", move
            exec_time = time.time() - self.start_time
            print "Solution found in %s seconds" % exec_time
            sys.exit(0)
            return
        if moves_left <= 0:
            #print "Out of moves!"
            return
        for region_name in regions:
            region = regions_map[region_name]
            for color in range(len(colors)):
                if region.color == color:
                    continue
                move = "Move %d: set %s to %s" % (moves_left, region.name, colors[color])
                #print move
                new_path = path[:] + [move]
                regions_c = regions[:]
                regions_map_c = {}
                for region_name_c in regions_map:
                    region_c = regions_map[region_name_c]
                    regions_map_c[region_name_c] = Region(region_c.name, region_c.color, set(list(region_c.adj)))
                region.set_color(color, regions_c, regions_map_c)
                self.solve_r(regions_c, regions_map_c, colors, moves_left-1, new_path)
    
    def print_regions(self):
        for region in self.regions_map.values():
            print "%s:%s  " % (region.name, self.colors[region.color]),
        print ""
           
def main():
    
    
    # Around 1 hr runtime
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
    kami.solve(2)
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
           
           
           
           
           
           
           
           
           
            
