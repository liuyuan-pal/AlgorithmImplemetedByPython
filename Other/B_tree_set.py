
M=30
'''
1. Empty entry produced by splitting will not be deleted, just marked as unused by h.m.
[h.m:M] are un unsed entries.
2. the children of k-th node (h.children[k].next) is in range: [h.children[k].key,h.children[k+1])
Exception:
    1) k=1 range: (MINIMUM_KEY,h.children[2].key)
    2) k=h.m-1 range: [h.children[h.m-1].key,MAXIMUM_KEY)
    
'''
class Node():
    def __init__(self,child_num=0):
        self.m=child_num                         # number of children
        self.children=[Entry(None) for _ in range(M)]   # children

class Entry():
    def __init__(self,key,next=None):
        self.key=key        # comparable
        self.next=next      # Node

class BTreeSet():
    def __init__(self):
        self.root=Node(0)
        self.height=0

    def contains(self,key):
        return self.search(self.root,key,self.height)

    def search(self,node,key,ht):
        children=node.children

        # external node
        if ht==0:
            for index in range(node.m):
                if children[index].key==key:
                    return True

            return False

        # internal node
        for index in range(node.m):
            if index+1==node.m or key<children[index+1].key:
                return self.search(children[index].next,key,ht-1)

        return False

    def add(self,key):
        u=self.insert(self.root,key,self.height)
        if u==None: return
        t=Node(2)
        t.children[0]=Entry(self.root.children[0].key,self.root)
        t.children[1]=Entry(u.children[0].key,u)
        self.root=t
        self.height+=1

    def insert(self,h,key,ht):
        j=0
        t=Entry(key)

        # external node
        if ht==0:
            for i in range(h.m):
                if key < h.children[i].key:
                    j=i
                    break
                # java implementation forgets this case
                elif key==h.children[i].key:
                    return None
            else:
                j=h.m

        # internal node
        else:
            for i in range(h.m):
                if i+1==h.m or key <h.children[i+1].key:
                    u=self.insert(h.children[i].next,key,ht-1)
                    j=i+1
                    if u==None: return None
                    t.key=u.children[0].key
                    t.next=u
                    break

        for i in range(h.m,j,-1):
            h.children[i]=h.children[i-1]
        h.children[j]=t
        h.m+=1
        if h.m<M: return None
        else: return self.split(h)

    def split(self,h):
        t=Node(M/2)
        h.m=M/2
        for j in range(M/2):
            t.children[j]=h.children[M/2+j]
        return t

def print_node(h,blank):
    print blank+str([child.key for child in h.children[0:h.m]])
    for i in range(0,h.m):
        if h.children[i].next is not None and h.children[i].next.m>0:
            print_node(h.children[i].next,blank+'\t')

if __name__ =="__main__":
    btree_set=BTreeSet()
    import random
    a=range(100000)
    random.shuffle(a)

    a=a[:10000]

    for i in a:
        btree_set.add(i)

    import time
    bg=time.clock()
    print btree_set.contains(0)
    print time.clock()-bg
    bg=time.clock()
    print 0 in a
    print time.clock()-bg

    print a[0]
    print btree_set.contains(a[0])

    print '--------------'
    print_node(btree_set.root,'')



