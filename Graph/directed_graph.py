class DiGraph:
    def __init__(self,V=None,In=None):

        self.adj_v = []
        self.V = 0
        self.E = 0

        if V is not None:
            self.adj_v=[[] for i in range(V)]
            self.V=V

        if In is not None:
            lines=In.readlines()
            self.V=int(lines[0])
            self.adj_v=[[] for i in range(self.V)]
            # self.E=int(lines[1])
            for line in lines[2:]:
                if len(line.strip())<=0:
                    continue
                v=int(line.strip().split()[0])
                w=int(line.strip().split()[1])

                self.add_edge(v,w)

    def adj(self,v):
        return self.adj_v[v]

    def add_edge(self,v,w):
        (self.adj_v[v]).append(w)
        self.E+=1

    def reverse(self):
        dg=DiGraph(self.V)
        for v in range(self.V):
            for w in self.adj(v):
                dg.add_edge(w,v)

        return dg

# find cycle
class DirectedCycle:
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
        for w in G.adj(v):
            if not self.marked[w]:
                self.edge_to[w]=v
                self.dfs(G,w)
            elif self.on_stack[w]:
                self.has_cycle=True
                x=v
                while x!=w:
                    self.cycle.append(x)
                    x=self.edge_to[x]

                self.cycle.append(w)
                self.cycle.append(v)

                self.cycle=self.cycle[::-1]

        self.on_stack[v]=False

# pre,post,reverse post search order
class DepthFirstOrder:
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
        for w in G.adj(v):
            if not self.marked[w]:
                self.dfs(G,w)
        self.post.append(v)

# find strongly connected component
class KosarajuSCC:
    def __init__(self,G):
        self.marked=[False for i in range(G.V)]
        self.id=[i for i in range(G.V)]
        dfo=DepthFirstOrder(G.reverse())
        self.count=0
        print dfo.reverse_post
        for v in dfo.reverse_post:
            if not self.marked[v]:
                self.dfs(G,v)
                self.count+=1

    def dfs(self,G,v):
        self.marked[v]=True
        self.id[v]=self.count
        for w in G.adj(v):
            if not self.marked[w]:
                self.dfs(G,w)


if __name__=='__main__':
    with open('tinyDG.txt') as f:
        g=DiGraph(V=None,In=f)

    print g.adj_v

    dc=DirectedCycle(g)
    print dc.has_cycle

    scc=KosarajuSCC(g)
    component=[]
    for i in range(scc.count):
        this_component=[]
        for j in range(g.V):
            if scc.id[j]==i:
                this_component.append(j)
        component.append(this_component)

    print component