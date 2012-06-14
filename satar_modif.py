################################################################################
#
#   Project: AStar Path Finding Algorithm
#
#   File: satar_modif.py
#
#   Author: John Eriksson
#
#   Website: http://arainyday.se/projects/python/AStar/
#
#   Description: a Python implementation of the A* path finding algorithm.
#   The original code only worked with vertical and horizontal movements,
#   but no dialogal movements where processed. This was modified by Pablo
#   Farias Navarro by implementing the tweaks specified by the user "badoli"
#   in the comments sections at: http://arainyday.se/projects/python/AStar/
#   all these modifications are commented with a hash.
#
#   License: No license (Public Domain)
#
################################################################################

class Path:
    def __init__(self,nodes, totalCost):
        self.nodes = nodes;
        self.totalCost = totalCost;

    def getNodes(self): 
        return self.nodes    

    def getTotalMoveCost(self):
        return self.totalCost

class Node:
    def __init__(self,location,mCost,lid,parent=None):
        self.location = location # where is this node located
        self.mCost = mCost # total move cost to reach this node
        self.parent = parent # parent node
        self.score = 0 # calculated score for this node
        self.lid = lid # set the location id - unique for each location in the map

    def __eq__(self, n):
        if n.lid == self.lid:
            return 1
        else:
            return 0

class AStar:

    def __init__(self,maphandler):
        self.mh = maphandler
                
    def _getBestOpenNode(self):
        bestNode = None        
        for n in self.on:
            if not bestNode:
                bestNode = n
            else:
                if n.score<=bestNode.score:
                    bestNode = n
        return bestNode

    def _tracePath(self,n):
        nodes = [];
        totalCost = n.mCost;
        p = n.parent;
        nodes.insert(0,n);       
        
        while 1:
            if p.parent is None: 
                break

            nodes.insert(0,p)
            p=p.parent
        
        return Path(nodes,totalCost)

    def _handleNode(self,node,end):        
        i = self.o.index(node.lid)
        self.on.pop(i)
        self.o.pop(i)
        self.c.append(node.lid)

        nodes = self.mh.getAdjacentNodes(node,end)
                   
        for n in nodes:
            if n.location == end:
                # reached the destination
                return n
            elif n.lid in self.c:
                # already in close, skip this
                continue
            elif n.lid in self.o:
                # already in open, check if better score
                i = self.o.index(n.lid)
                on = self.on[i];
                if n.mCost<on.mCost:
                    self.on.pop(i);
                    self.o.pop(i);
                    self.on.append(n);
                    self.o.append(n.lid);
            else:
                # new node, append to open list
                self.on.append(n);                
                self.o.append(n.lid);

        return None

    def findPath(self,fromlocation, tolocation):
        self.o = []
        self.on = []
        self.c = []

        end = tolocation
        fnode = self.mh.getNode(fromlocation,1)
        self.on.append(fnode)
        self.o.append(fnode.lid)
        nextNode = fnode 
               
        while nextNode is not None: 
            finish = self._handleNode(nextNode,end)
            if finish:                
                return self._tracePath(finish)
            nextNode=self._getBestOpenNode()
                
        return None
      
class SQ_Location:
    """A simple Square Map Location implementation"""
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __eq__(self, l):
        """MUST BE IMPLEMENTED"""
        if l.x == self.x and l.y == self.y:
            return 1
        else:
            return 0

class SQ_MapHandler:
    """A simple Square Map implementation"""

    def __init__(self,mapdata,width,height):
        self.m = mapdata
        self.w = width
        self.h = height

    def getNode(self, location,multi):
        """MUST BE IMPLEMENTED"""
        x = location.x
        y = location.y
        if x<0 or x>=self.w or y<0 or y>=self.h:
            return None
        d = self.m[(y*self.w)+x]
        if d == -1:
            return None

        d=d*multi

        return Node(location,d,((y*self.w)+x));                

    def getAdjacentNodes(self, curnode, dest):
        """MUST BE IMPLEMENTED"""        
        result = []
       
        cl = curnode.location
        dl = dest
        
         # Hor. and Vert. nodes
        n = self._handleNode(cl.x+1,cl.y,curnode,dl.x,dl.y,1) # multi is 1
        if n: result.append(n)
        n = self._handleNode(cl.x-1,cl.y,curnode,dl.x,dl.y,1)
        if n: result.append(n)
        n = self._handleNode(cl.x,cl.y+1,curnode,dl.x,dl.y,1)
        if n: result.append(n)
        n = self._handleNode(cl.x,cl.y-1,curnode,dl.x,dl.y,1)
        if n: result.append(n)

        #Diagonal nodes
        n = self._handleNode(cl.x+1,cl.y+1,curnode,dl.x,dl.y,1.4142) # multi is 1.4142
        if n: result.append(n)
        n = self._handleNode(cl.x-1,cl.y-1,curnode,dl.x,dl.y,1.4142)
        if n: result.append(n)
        n = self._handleNode(cl.x-1,cl.y+1,curnode,dl.x,dl.y,1.4142)
        if n: result.append(n)
        n = self._handleNode(cl.x+1,cl.y-1,curnode,dl.x,dl.y,1.4142)
        if n: result.append(n)

        return result

    def _handleNode(self,x,y,fromnode,destx,desty,multi):
        # multi would be 1 for hor. and vert. nodes, 1.4142 for diagonal
        n = self.getNode(SQ_Location(x,y),multi)
        if n is not None:
            dx = max(x,destx) - min(x,destx)
            dy = max(y,desty) - min(y,desty)
            emCost = dx+dy
            n.mCost += fromnode.mCost                                   
            n.score = n.mCost+emCost
            n.parent=fromnode
            return n

        return None    
