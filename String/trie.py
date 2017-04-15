R=10

class Node:
    def __init__(self,val=None):
        self.val=val
        self.next=[None for _ in range(R)]

def get_ch(key,d):
    return int(key[d])

class Trie:
    def __init__(self):
        self.root=None

    def get(self,key):
        return self.get_impl(self.root,key,0)

    def put(self,key,val):
        self.root=self.put_impl(self.root,key,val,0)

    def get_impl(self,node,key,d):
        if node is None:
            return None
        if d==len(key):
            return node.val
        return self.get_impl(node.next[get_ch(key,d)],key,d+1)

    def put_impl(self,node,key,val,d):
        if node is None:
            node=Node()
        if len(key)==d:
            node.val=val
        else:
            index=get_ch(key,d)
            node.next[index]=self.put_impl(node.next[index],key,val,d+1)
        return node

    def delete(self,key):
        self.root=self.del_impl(self.root,key,0)


    def del_impl(self,node,key,d):
        if node is None:
            return None
        if len(key)==d:
            node.val=None
        else:
            index = get_ch(key, d)
            node.next[index]=self.del_impl(node.next[index],key,d+1)
        for next in node.next:
            if next is not None: return node
        return None

if __name__ == "__main__":

    t=Trie()
    t.put('1234',500)
    t.put('12342',3500)
    t.put('12342',1500)
    t.put('12341',4500)
    print t.get('12342')
    t.delete('1234')

    print t.get('12341')
