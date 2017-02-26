
def min_sink(a, index, N):
    while index*2<=N:
        child_index=index*2
        if child_index < N and a[child_index] > a[child_index + 1]:
            child_index += 1

        if a[index] > a[child_index]:
            a[index], a[child_index] = a[child_index], a[index]
            index=child_index
        else:
            break


def min_swim(a, index, N):
    while index/2>0 and a[index] < a[index/2]:
        a[index], a[index/2] = a[index/2], a[index]
        index/=2


class MinPQ:
    def __init__(self):
        self.size=0
        self.a=[None]

    def put(self,key):
        self.a.append(key)
        self.size+=1
        min_swim(self.a,self.size,self.size)

    def delete_min(self):
        self.a[1],self.a[self.size]=self.a[self.size],self.a[1]
        self.size-=1
        min_sink(self.a,1,self.size)
        return self.a.pop()

    def __len__(self):
        return self.size

if __name__=='__main__':
    import numpy as np
    tmp=np.random.choice(10,10,False)
    min_pq=MinPQ()
    print tmp
    for num in tmp:
        min_pq.put(num)

    for num in tmp:
        print min_pq.delete_min()


