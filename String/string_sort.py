import numpy as np
import random

R=10 # th size of alphabet

def generate_fixed_length_str(str_len,str_num):
    str_list=[]
    for i in range(str_num):
        ran_str=''.join(['{}'.format(random.randint(0,9)) for _ in range(str_len)])
        str_list.append(ran_str)
    return str_list

def LSD(str_list):
    N=len(str_list)
    aux=[None for _ in str_list]
    W=len(str_list[0])
    for i in range(W-1,-1,-1):

        str_count = [0 for _ in range(R + 1)]

        # count
        for j in range(N):
            str_count[int(str_list[j][i])+1]+=1

        # sum
        for j in range(0,R):
            str_count[j+1]+=str_count[j]


        # sort
        for j in range(N):
            aux[str_count[int(str_list[j][i])]]=str_list[j]
            str_count[int(str_list[j][i])]+=1

        # swap
        str_list=[str(str_num) for str_num in aux]

    return aux

def get_ch(s,d):
    if d<len(s):
        return int(s[d])
    else:
        return -1

def MSD(a):
    aux=[None for _ in a]
    MSD_impl(a,0,len(a)-1,0,aux)

def MSD_impl(a,lo,hi,d,aux):

    if lo>=hi:
        return

    count=[0 for _ in range(R+2)]

    for i in range(lo,hi+1):
        count[get_ch(a[i],d)+2]+=1

    # sum
    for j in range(0, R+1):
        count[j + 1] += count[j]

    # sort
    for i in range(lo,hi+1):
        ch_val=get_ch(a[i], d) + 1
        index_val=count[ch_val]
        aux[index_val],a[i]=a[i],aux[index_val]
        count[ch_val]+=1

    for i in range(lo,hi+1):
        a[i],aux[i-lo]=aux[i-lo],a[i]

    for r in range(R):
        MSD_impl(a,lo+count[r],lo+count[r+1]-1,d+1,aux)


if __name__=="__main__":
    str_list=generate_fixed_length_str(10,50000)
    import time
    bg=time.clock()
    sorted(str_list)
    print 'sort costs {}s'.format(time.clock()-bg)

    bg=time.clock()
    MSD(str_list)
    print 'LSD costs {}s'.format(time.clock()-bg)