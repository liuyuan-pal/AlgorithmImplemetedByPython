class Edge:
    def __init__(self,w,v,weight):
        self.w=w
        self.v=v
        self.weight=weight

    def __cmp__(self, other):
        if self.weight>other:
            return 1
        elif self.weight<other:
            return -1
        else:
            return 0

    def __str__(self):
        return '{},{},{}'.format(self.v,self.w,self.weight)

    def other(self, x):
        if x==self.v:
            return self.w
        if x==self.w:
            return self.v

    def either(self):
        return self.v

class WeightedGraph:
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
        e=Edge(v, w, weight)
        (self.adj_v[v]).append(e)
        (self.adj_v[w]).append(e)
        self.edges.append(e)
        self.E+=1



import sys
sys.path.append('..')
from Sort.prior_queue import MinPQ

# delete delay prim algorithm
class LazyPrimMST:
    def __init__(self,G):
        self.pq=MinPQ()
        self.marked=[False for i in range(G.V)]
        self.mst=[]
        self.visit(G,0)
        while len(self.pq)>0:
            e=self.pq.delete_min()
            v=e.either()
            w=e.other(v)
            if self.marked[v] and self.marked[w]:
                continue
            self.mst.append(e)
            if not self.marked[v]:
                self.visit(G,v)
            if not self.marked[w]:
                self.visit(G,w)

    def visit(self,G,s):
        self.marked[s]=True
        for e in G.adj(s):
            if not self.marked[e.other(s)]:
                self.pq.put(e)

# a index min prior queue
class IndexMinPQ:

    def larger(self,i,j):
        return self.vals[self.index_pq[i]] > self.vals[self.index_pq[j]]

    def exch(self,i,j):
        self.reverse_pq[self.index_pq[i]], self.reverse_pq[self.index_pq[j]] \
            = self.reverse_pq[self.index_pq[j]], self.reverse_pq[self.index_pq[i]]
        self.index_pq[i],self.index_pq[j]=self.index_pq[j],self.index_pq[i]

    def swim(self,k,N):
        while k/2>0 and self.larger(k/2,k):
            self.exch(k/2,k)
            k=k/2

    def sink(self,k,N):
        while 2*k<=N:
            j=2*k
            if j<N and self.larger(j,j+1):
                j+=1
            if self.larger(k,j):
                self.exch(j,k)
                k=j
            else:
                break


    def __init__(self,max_size):
        self.max_size=max_size
        self.vals=[None for i in range(max_size)]
        self.index_pq=[None]
        self.reverse_pq=[None for i in range(max_size)]
        self.size=0
        self.existence=[-1 for i in range(max_size)]

    def insert(self,key,val):
        self.size+=1
        self.vals[key]=val
        self.existence[key]=1
        self.index_pq.append(key)
        self.reverse_pq[key]=self.size
        self.swim(self.size,self.size)

    def change(self,key,val):
        self.vals[key]=val
        self.swim(self.reverse_pq[key],self.size)
        self.sink(self.reverse_pq[key],self.size)

    def contains(self,key):
        return self.existence[key]>0

    def delete_min(self):
        self.exch(1,self.size)
        min_index=self.index_pq.pop()
        self.vals[min_index]=None
        self.reverse_pq[min_index]=None
        self.existence[min_index]=None
        self.size-=1
        self.sink(1,self.size)
        return min_index

    def __len__(self):
        return self.size

# prim minimum spanning tree
import sys
class PrimMST:
    def __init__(self,G):
        self.pq=IndexMinPQ(G.V)
        self.edge_to=[None for i in range(G.V)]
        self.dist_to=[sys.float_info.max for i in range(G.V)]
        self.marked=[False for i in range(G.V)]
        self.mst=[]

        self.dist_to[0]=0
        self.edge_to[0]=0
        self.visit(G,0)

        while len(self.pq)>0:
            index=self.pq.delete_min()
            self.mst.append(self.edge_to[index])
            self.visit(G,index)

    def visit(self,G,s):
        self.marked[s]=True
        for e in G.adj(s):
            v=e.other(s)
            if not self.marked[v]:
                if e.weight<self.dist_to[v]:
                    self.dist_to[v]=e.weight
                    self.edge_to[v]=e
                    if self.pq.contains(v):
                        self.pq.change(v,self.dist_to[v])
                    else:
                        self.pq.insert(v,self.dist_to[v])

from UnionFind.unionfind import UF
class KruskalMST:
    def __init__(self,G):
        self.pq=MinPQ()
        self.uf=UF(G.V,'weighted quick union')
        self.mst=[]

        for e in G.edges:
            self.pq.put(e)

        while len(self.pq)>0 and len(self.mst)<G.V-1:
            e=self.pq.delete_min()
            v=e.either()
            w=e.other(v)
            if not self.uf.connected(v,w):
                self.uf.union(v,w)
                self.mst.append(e)




if __name__=='__main__':
    with open('mediumEWG.txt') as f:
        g=WeightedGraph(V=None,In=f)

    # print g.adj_v

    lpMST=KruskalMST(g)
    weight_sum=0
    for e in lpMST.mst:
        weight_sum+=e.weight
        print e

    print weight_sum

    # import numpy as np
    # t=np.random.choice(10,10,False)
    # pq=IndexMinPQ(10)
    # for i,j in zip(range(10),t):
    #     pq.insert(i,j)
    #
    # pq.change(3,100)
    # pq.change(7,1000)
    # t[3]=100
    # t[7]=1000
    # print t
    # print np.argsort(t)
    #
    # for i in range(10):
    #     print pq.delete_min()

