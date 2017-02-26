class ST:

    class Node:
        def __init__(self,key,val,N,left=None,right=None):
            self.key=key
            self.val=val
            self.left=left
            self.right=right
            self.N=N

    @staticmethod
    def size_node(node):
        if node is None:
            return 0
        else:
            return node.N

    def __init__(self):
        self.root=None

    def put_impl(self,node,key,val):
        if node is None:
            return self.Node(key,val,1)
        if key==node.key:
            node.val=val
        elif key<node.key:
            node.left=self.put_impl(node.left,key,val)
        else:
            node.right=self.put_impl(node.right,key,val)
        node.N=self.size_node(node.left)+self.size_node(node.right)+1
        return node

    def put(self,key,val):
        self.root=self.put_impl(self.root,key,val)

    def get_impl(self,node,key):
        if node==None:
            return None
        if key==node.key:
            return node.val
        elif key<node.key:
            return self.get_impl(node.left,key)
        else:
            return self.get_impl(node.right,key)

    def get(self,key):
        return self.get_impl(self.root,key)

    def delete_min_impl(self,node):
        if node.left is None:
            return node.right
        node.left=self.delete_min_impl(node.left)
        node.N=self.size_node(node.left)+self.size_node(node.right)+1
        return node

    def min_impl(self,node):
        if node.left is not None:
            return self.min_impl(node.left)
        else:
            return node

    def delete_impl(self,node,key):
        if node is None:
            return None
        if key>node.key:
            node.right=self.delete_impl(node.right,key)
        elif key<node.key:
            node.left=self.delete_impl(node.left,key)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            else:
                t=self.min_impl(node.right)
                t.left=node.left
                t.right=self.delete_min_impl(node.right)
                node=t

            node.N=self.size_node(node.left)+self.size_node(node.right)+1
            return node

    def contains(self,key):
        return self.get(key) is not None

    def delete(self,key):
        self.delete_impl(self.root,key)

RED=1
BLACK=0
class RedBlackST:

    class Node:
        def __init__(self,key,val,N,color,left=None,right=None):
            self.key=key
            self.val=val
            self.left=left
            self.right=right
            self.N=N
            self.color=color

    @staticmethod
    def size_node(node):
        if node is None:
            return 0
        else:
            return node.N

    def __init__(self):
        self.root=None

    @staticmethod
    def left_rotate(node):
        x=node.right
        node.right=x.left
        x.left=node

        x.color=node.color
        node.color=RED

        x.N=node.N
        node.N=RedBlackST.size_node(node.left)+RedBlackST.size_node(node.right)+1

        return x

    @staticmethod
    def right_rotate(node):
        x=node.left
        node.left=x.right
        x.right=node

        x.color=node.color
        node.color=RED

        x.N=node.N
        node.N=RedBlackST.size_node(node.left)+RedBlackST.size_node(node.right)+1

        return x

    @staticmethod
    def flip_color(node):
        node.color=RED
        node.left.color=BLACK
        node.right.color=BLACK

    @staticmethod
    def is_red(node):
        if node is not None:
            return node.color==RED
        else:
            return False

    def put_impl(self,node,key,val):
        if node is None:
            return self.Node(key,val,1,RED)
        if key==node.key:
            node.val=val
        elif key<node.key:
            node.left=self.put_impl(node.left,key,val)
        else:
            node.right=self.put_impl(node.right,key,val)

        if self.is_red(node.right) and not self.is_red(node.left):
            node=self.left_rotate(node)
        if self.is_red(node.left) and self.is_red(node.left.left):
            node=self.right_rotate(node)
        if self.is_red(node.left) and self.is_red(node.right):
            self.flip_color(node)

        node.N=self.size_node(node.left)+self.size_node(node.right)+1
        return node

    def put(self,key,val):
        self.root=self.put_impl(self.root,key,val)

    def get_impl(self,node,key):
        if node==None:
            return None
        if key==node.key:
            return node.val
        elif key<node.key:
            return self.get_impl(node.left,key)
        else:
            return self.get_impl(node.right,key)

    def get(self,key):
        return self.get_impl(self.root,key)

    def contains(self,key):
        return self.get(key) is not None

    @staticmethod
    def move_red_left(h):
        RedBlackST.flip_color(h)
        if RedBlackST.is_red(h.right.left):
            h.right=RedBlackST.right_rotate(h.right)
            h=RedBlackST.left_rotate(h)
            RedBlackST.flip_color(h)

        return h


    @staticmethod
    def move_red_right(h):
        RedBlackST.flip_color(h)
        if RedBlackST.is_red(h.left.left):
            h=RedBlackST.right_rotate(h)
            RedBlackST.flip_color(h)

        return h

    @staticmethod
    def balance(h):
        if RedBlackST.is_red(h.right):
            h=RedBlackST.left_rotate(h)
        if RedBlackST.is_red(h.left)\
            and RedBlackST.is_red(h.left.left):
            h=RedBlackST.right_rotate(h)
        if RedBlackST.is_red(h.left)\
            and RedBlackST.is_red(h.right):
            RedBlackST.flip_color(h)

        h.N=RedBlackST.size_node(h.left)+RedBlackST.size_node(h.right)+1
        return h

    @staticmethod
    def delete_min_impl(h):
        if h.left is None:
            return None

        if not RedBlackST.is_red(h.left) \
            and not RedBlackST.is_red(h.left.left):
            h=RedBlackST.move_red_left(h)

        h.left=RedBlackST.delete_min_impl(h.left)
        return RedBlackST.balance(h)


    def delete_min(self):
        if self.root is None:
            return

        if not self.is_red(self.root.left) \
            and not self.is_red(self.root.right):
            self.root.color=RED

        self.root=self.delete_min_impl(self.root)

        if self.root is not None:
            self.root.color=BLACK

    @staticmethod
    def delete_impl(h,key):
        if key<h.key:
            if not RedBlackST.is_red(h.left) and\
                not RedBlackST.is_red(h.left.left):
                h=RedBlackST.move_red_left(h)
            h.left=RedBlackST.delete_impl(h.left,key)
        else:
            if RedBlackST.is_red(h.left):
                h=RedBlackST.right_rotate(h)
            if key==h.key and h.right is None:
                return None
            if not RedBlackST.is_red(h.right) and\
                not RedBlackST.is_red(h.right.left):
                h=RedBlackST.move_red_right(h)
            if key==h.key:
                x=RedBlackST.min_impl(h.right)
                h.key=x.key
                h.val=x.val
                h.right=RedBlackST.delete_min_impl(h.right)
            else:
                h.right=RedBlackST.delete_impl(h.right,key)

        return RedBlackST.balance(h)

    @staticmethod
    def min_impl(h):
        if h.left is None:
            return h
        else:
            RedBlackST.min_impl(h.left)

    def min(self):
        if self.root is None:
            return None
        return self.min_impl(self.root).val

    def delete(self,key):

        if not self.contains(key):
            return

        if not self.is_red(self.root.left) \
            and not self.is_red(self.root.right):
            self.root.color=RED

        self.root=self.delete_impl(self.root,key)
        if self.root is not None:
            self.root.color=BLACK



def test_frequency_counter(test_ST):
    # frequency counter
    import time
    st=test_ST()
    min_len=4
    with open('wordlist.txt') as f:
        for lines in f.readlines():
            word_list=lines.split(' ')
            for word in word_list:
                filtered_word=filter(str.isalpha,word)
                if len(filtered_word)>min_len:
                    filtered_word=str.lower(filtered_word)
                    # print filtered_word
                    old_val=st.get(filtered_word)
                    if old_val is not None:
                        st.put(filtered_word,old_val+1)
                    else:
                        st.put(filtered_word,1)

    # query frequency
    bg=time.clock()
    print 'busines frequency:{}'.format(st.get('busines'))
    print 'time used:{}s'.format(time.clock()-bg)

    bg=time.clock()
    print 'ababdeh frequency:{}'.format(st.get('ababdeh'))
    print 'time used:{}s'.format(time.clock()-bg)

    bg=time.clock()
    st.delete_min()
    print 'ababdeh frequency:{}'.format(st.get('ababdeh'))
    print 'time used:{}s'.format(time.clock()-bg)

    bg=time.clock()
    st.delete('busines')
    print 'busines frequency:{}'.format(st.get('busines'))
    print 'time used:{}s'.format(time.clock()-bg)

    bg=time.clock()
    print 'busket frequency:{}'.format(st.get('busket'))
    print 'time used:{}s'.format(time.clock()-bg)




if __name__=='__main__':
    # test_frequency_counter(ST)
    test_frequency_counter(RedBlackST)