import numpy as np


class UF:
    def __init__(self,N,mode):
        self.id=range(N)
        self.count=N
        self.mode=mode
        self.size=list(np.ones(N))

    def get_count(self):
        return self.count

    def find(self,p):
        if self.mode=='quick find':
            return self.id[p]
        elif self.mode=='quick union' or self.mode == 'weighted quick union':
            if self.id[p]!=p:
                return self.find(self.id[p])
            else:
                return p
        elif self.mode=='path compression':
            if self.id[p]!=p:
                origin=self.find(self.id[p])
                self.id[p]=origin
                return origin
            else:
                return p

    def union(self,p,q):
        if self.mode=='quick find':
            pclass=self.id[p]
            qclass=self.id[q]

            if pclass==qclass:
                return

            for index,id in enumerate(self.id):
                if id == qclass:
                    self.id[index]=pclass
            self.count-=1
        elif self.mode=='quick union':
            pclass=self.find(p)
            qclass=self.find(q)
            if pclass!=qclass:
                self.id[qclass]=pclass
                self.count-=1
        elif self.mode=='weighted quick union' or self.mode=='path compression':
            pclass=self.find(p)
            qclass=self.find(q)
            if pclass!=qclass:
                if self.size[pclass]>self.size[qclass]:
                    self.id[qclass]=pclass
                    self.size[pclass]+=self.size[qclass]
                else:
                    self.id[pclass]=qclass
                    self.size[qclass]+=self.size[pclass]

                self.count-=1

    def connected(self,p,q):
        return self.find(p)==self.find(q)

def test_UF(file_name,mode_name):
    time_begin=time.clock()
    with open(file_name) as file:
        for line_num,line in enumerate(file.readlines()):
            if len(line)<1:
                break
            if line_num==0:
                uf=UF(int(line),mode_name)
                continue

            p=int(line.split(' ')[0])
            q=int(line.split(' ')[1])
            uf.union(p,q)

        print 'component:{}'.format(uf.count)
    print 'path compression time cost:{} s'.format(time.clock()-time_begin)

if __name__=='__main__':
    import time
    file_name='largeUF.txt'
    test_UF(file_name,'path compression')
    test_UF(file_name,'weighted quick union')
