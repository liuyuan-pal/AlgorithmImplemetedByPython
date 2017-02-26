class DirectedEdge:
    def __init__(self,v,w,weight):
        self.v=v
        self.w=w
        self.weight=weight


class WeightedDigraph:
    def __init__(self,V,In):
        self.adj_v = []
        self.V = 0
        self.E = 0
        self.edges=[]

        if V is not None:
            self.adj_v=[[] for i in range(V)]
            self.V=V

        if In is not None:
            lines=In.readlines()
            self.V=int(lines[0])
            self.adj_v=[[] for i in range(self.V)]
            # self.E=int(lines[1])
            for line in lines[2:]:
                v=int(line.strip().split()[0])
                w=int(line.strip().split()[1])
                weight=float(line.strip().split()[2])
                self.add_edge(v,w,weight)

    def adj(self,v):
        return self.adj_v[v]

    def add_edge(self,v,w,weight):
        e=DirectedEdge(v, w, weight)
        self.adj_v[v].append(e)
        self.edges.append(e)
        self.E+=1

from minimum_spanning_tree import IndexMinPQ
import sys


class DijkstraSP:
    def __init__(self, G, s):
        self.pq = IndexMinPQ(G.V)
        self.edge_to = [None for i in range(G.V)]
        # self.marked=[False for i in range(G.V)]
        self.dist_to = [sys.float_info.max for i in range(G.V)]

        self.dist_to[s] = 0
        self.s = s

        self.pq.insert(s, self.dist_to[s])
        self.edge_to[s] = s

        while len(self.pq) > 0:
            v = self.pq.delete_min()
            self.relax(G, v)


    def relax(self,G,s):
        # self.marked[s]=True
        for e in G.adj(s):
            # if not self.marked[e.w]:
            if e.weight+self.dist_to[s]<self.dist_to[e.w]:
                self.dist_to[e.w]=e.weight+self.dist_to[s]
                self.edge_to[e.w]=e
                if self.pq.contains(e.w):
                    self.pq.change(e.w,e.weight)
                else:
                    self.pq.insert(e.w,e.weight)

    def has_path_to(self,v):
        return self.dist_to[v]!=sys.float_info.max

    def path_to(self,v):
        path=[]
        while v!=self.s:
            path.append(v)
            v=self.edge_to[v].v

        path.append(self.s)
        return path[::-1]

class DiEdgeWeightedCycle:
    def __init__(self,G):
        self.marked=[False for i in range(G.V)]
        self.has_cycle=False
        self.edge_to=[None for i in range(G.V)]
        self.cycle=[]
        self.on_stack=[False for i in range(G.V)]
        for s in range(G.V):
            if not self.marked[s]:
                self.dfs(G,s)


    def dfs(self,G,v):
        if self.has_cycle:
            return
        self.marked[v]=True
        self.on_stack[v]=True
        for e in G.adj(v):
            if not self.marked[e.w]:
                self.edge_to[e.w]=v
                self.dfs(G,e.w)
            elif self.on_stack[e.w]:
                self.has_cycle=True
                x=v
                while x!=e.w:
                    self.cycle.append(x)
                    x=self.edge_to[x]

                self.cycle.append(e.w)
                self.cycle.append(v)

                self.cycle=self.cycle[::-1]

        self.on_stack[v]=False



class BellmanFordSP:
    def __init__(self,G,s):
        self.queue=[]
        self.edge_to=[None for i in range(G.V)]
        self.dist_to=[sys.float_info.max for i in range(G.V)]
        self.on_queue=[False for i in range(G.V)]
        self.count=0
        self.has_negative_cycle=False

        self.dist_to[s]=0
        self.s=s

        self.queue.append(s)
        self.edge_to[s]=None
        self.on_queue[s]=True

        while len(self.queue)>0 and not self.has_negative_cycle:
            v=self.queue.pop(0)
            self.relax(G,v)
            self.on_queue[v]=False


    def relax(self,G,s):
        for e in G.adj(s):

            if e.weight+self.dist_to[s]<self.dist_to[e.w]:
                self.dist_to[e.w]=e.weight+self.dist_to[s]
                self.edge_to[e.w]=e
                if not self.on_queue[e.w]:
                    self.queue.append(e.w)
                    self.on_queue[e.w]=True

            if self.count%G.V==0:
                self.find_negative_cycle()

            self.count+=1


    def has_path_to(self,v):
        return self.dist_to[v]!=sys.float_info.max

    def path_to(self,v):
        path=[]
        while v!=self.s:
            path.append(v)
            v=self.edge_to[v].v

        path.append(self.s)
        return path[::-1]

    def find_negative_cycle(self):
        V=len(self.edge_to)
        wd=WeightedDigraph(V=V,In=None)
        for v in range(V):
            if self.edge_to[v] is not None:
                wd.add_edge(self.edge_to[v].v,self.edge_to[v].w,self.edge_to[v].weight)

        dewc=DiEdgeWeightedCycle(wd)
        self.has_negative_cycle=dewc.has_cycle
        self.cycle=dewc.cycle



class DepthFirstOrderWeightedDirected:
    def __init__(self,G):
        self.marked=[False for i in range(G.V)]
        self.pre=[]
        self.post=[]
        for s in range(G.V):
            if not self.marked[s]:
                self.dfs(G,s)
        self.reverse_post=self.post[::-1]


    def dfs(self,G,v):
        self.marked[v]=True
        self.pre.append(v)
        for e in G.adj(v):
            w=e.w
            if not self.marked[w]:
                self.dfs(G,w)
        self.post.append(v)

class AcyclicSP:
    def __init__(self,G,s):
        self.edge_to=[None for i in range(G.V)]
        self.dist_to=[sys.float_info.max for i in range(G.V)]

        self.dist_to[s]=0
        self.s=s
        self.edge_to[s]=s

        for v in DepthFirstOrderWeightedDirected(g).reverse_post:
            self.relax(G,v)


    def relax(self,G,s):
        for e in G.adj(s):
            if e.weight+self.dist_to[s]<self.dist_to[e.w]:
                self.dist_to[e.w]=e.weight+self.dist_to[s]
                self.edge_to[e.w]=e

    def has_path_to(self,v):
        return self.dist_to[v]!=sys.float_info.max

    def path_to(self,v):
        path=[]
        while v!=self.s:
            path.append(v)
            v=self.edge_to[v].v

        path.append(self.s)
        return path[::-1]


if __name__=='__main__':
    with open('tinyEWDnc.txt') as f:
        g=WeightedDigraph(V=None,In=f)

    # print g.adj_v

    sp=BellmanFordSP(g,5)
    for i in range(g.V):
        if sp.has_path_to(i):
            print sp.path_to(i)

    print sp.cycle
