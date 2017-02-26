class Graph:
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
                v=int(line.split(' ')[0])
                w=int(line.split(' ')[1])
                self.add_edge(v,w)

    def v_num(self):
        return self.V

    def e_num(self):
        return self.E

    def adj(self,v):
        return self.adj_v[v]

    def add_edge(self,v,w):
        (self.adj_v[v]).append(w)
        (self.adj_v[w]).append(v)
        self.E+=1

# depth first search path
class Path:
    def __init__(self,G,s):
        self.s=s
        self.edge_to=[None for i in range(G.V)]
        self.edge_to[s]=s
        self.marked=[False for i in range(G.V)]
        self.dfs(G,s)

    def dfs(self,G,s):
        self.marked[s]=True
        for v in G.adj(s):
            if not self.marked[v]:
                self.edge_to[v]=s
                self.dfs(G,v)

    def has_path_to(self,v):
        return self.marked[v]

    def path_to(self,v):
        if self.has_path_to(v):
            result=[]
            result.append(v)
            while self.edge_to[v]!=self.s:
                v=self.edge_to[v]
                result.append(v)
            result.append(self.s)
            return result[::-1]
        else:
            return None

# breadth first search path
class BFPath:
    def __init__(self,G,s):
        self.s=s
        self.edge_to=[None for i in range(G.V)]
        self.edge_to[s]=s
        self.marked=[False for i in range(G.V)]
        self.bfs(G,s)

    def bfs(self,G,s):
        daque=[]
        daque.append(s)
        self.marked[s]=True
        while len(daque)>0:
            v=daque.pop(0)
            for w in G.adj(v):
                if not self.marked[w]:
                    self.marked[w]=True
                    daque.append(w)
                    self.edge_to[w]=v



    def has_path_to(self,v):
        return self.marked[v]

    def path_to(self,v):
        if self.has_path_to(v):
            result=[]
            result.append(v)
            while self.edge_to[v]!=self.s:
                v=self.edge_to[v]
                result.append(v)
            result.append(self.s)
            return result[::-1]
        else:
            return None

# connected component
class CC:
    def __init__(self,G):
        self.marked=[False for i in range(G.V)]
        self.id=[i for i in range(G.V)]
        self.count=0
        for i in range(G.V):
            if not self.marked[i]:
                self.bfs(G,i)
                self.count+=1

    def bfs(self,G,s):
        daque=[]
        daque.append(s)
        self.marked[s]=True
        self.id[s]=self.count
        while len(daque)>0:
            v=daque.pop(0)
            for w in G.adj(v):
                if not self.marked[w]:
                    self.marked[w]=True
                    self.id[w]=self.count
                    daque.append(w)

    def connected(self,v,w):
        return self.id[v]==self.id[w]

# test cycle existence
class Cycle:

    def __init__(self,G):
        self.marked=[False for i in range(G.V)]
        self.has_cycle=False
        for s in range(G.V):
            if not self.marked[s]:
                self.dfs(G,s,s)


    def dfs(self,G,v,u):
        self.marked[v]=True
        for w in G.adj(v):
            if not self.marked[w]:
                self.dfs(G,w,v)
            elif w!=u:
                self.has_cycle=True

# test is two colorable
class TwoColor:

    def __init__(self,G):
        self.marked=[False for i in range(G.V)]
        self.two_colorable=True
        self.color=[False for i in range(G.V)]
        for s in range(G.V):
            if not self.marked[s]:
                self.dfs(G,s)

    def dfs(self,G,v):
        self.marked[v]=True
        for w in G.adj(v):
            if not self.marked[w]:
                self.color[w]=not self.color[v]
                self.dfs(G,w)

            elif self.color[w]==self.color[v]:
                self.two_colorable=False


if __name__=='__main__':
    with open('tinyG.txt') as f:
        g=Graph(V=None,In=f)

    print g.adj_v

    cc=CC(g)
    component=[]
    for i in range(cc.count):
        this_component=[]
        for j in range(g.V):
            if cc.id[j]==i:
                this_component.append(j)
        component.append(this_component)

    print component
    print 'count:{}'.format(cc.count)
