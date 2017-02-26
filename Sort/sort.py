def select_sort(a):
    list_len = len(a)
    for i in range(list_len):
        min_index = i
        for j in range(i, list_len):
            if a[j] < a[min_index]:
                min_index = j

        a[i], a[min_index] = a[min_index], a[i]


def insert_sort(a):
    list_len = len(a)
    for i in range(1, list_len):
        for j in range(i, 0, -1):
            if a[j] < a[j - 1]:
                a[j], a[j - 1] = a[j - 1], a[j]
            else:
                break


def bubble_sort(a):
    list_len = len(a)
    for i in range(list_len - 1, 0, -1):
        for j in range(0, i):
            if a[j + 1] < a[j]:
                a[j], a[j + 1] = a[j + 1], a[j]


def shell_sort(a):
    list_len = len(a)
    h = 1
    while h < list_len / 3:
        h = h * 3 + 1
    while h >= 1:
        for i in range(h, list_len):
            for j in range(i, h - 1, -h):
                if a[j] < a[j - h]:
                    a[j], a[j - h] = a[j - h], a[j]
                else:
                    break
        h -= 1
        h /= 3


def merge(a, lo, mid, hi):
    i = lo
    j = mid + 1
    aux = a[:]
    for k in range(lo, hi + 1):
        if i > mid:
            a[k] = aux[j]
            j += 1
        elif j > hi:
            a[k] = aux[i]
            i += 1
        elif aux[i] < aux[j]:
            a[k] = aux[i]
            i += 1
        else:
            a[k] = aux[j]
            j += 1


def merge_sort_impl(a, lo, hi):
    if hi <= lo:
        return
    mid = lo + (hi - lo) / 2
    merge_sort_impl(a, lo, mid)
    merge_sort_impl(a, mid + 1, hi)
    merge(a, lo, mid, hi)


def merge_sort_b2u(a):
    length = len(a)
    sz = 1
    while sz < length:
        for i in range(0, length, 2 * sz):
            merge(a, i, i + sz - 1, min(i + 2 * sz - 1, length - 1))
        sz *= 2


def partition(a, lo, hi):
    i = lo + 1
    j = hi
    val = a[lo]
    while True:
        while a[i] < val:
            if i == hi:
                break
            i += 1
        while a[j] > val:
            if j == lo:
                break
            j -= 1
        if i >= j:
            break
        a[i], a[j] = a[j], a[i]

    a[lo], a[j] = a[j], a[lo]
    return j


def quick_sort_impl(a, lo, hi):
    if hi <= lo:
        return

    j = partition(a, lo, hi)
    quick_sort_impl(a, lo, j - 1)
    quick_sort_impl(a, j + 1, hi)


def quick_sort(a):
    import random
    random.shuffle(a)
    quick_sort_impl(a, 0, len(a) - 1)


def merge_sort(a):
    return merge_sort_impl(a, 0, len(a) - 1)


def swim(a, k):
    while k > 1 and a[k] > a[k / 2]:
        a[k], a[k / 2] = a[k / 2], a[k]
        k /= 2


def sink(a, k, N):
    while k * 2 <= N:
        j = k * 2
        if j < N and a[j] < a[j + 1]:
            j += 1
        if a[j] > a[k]:
            a[j], a[k] = a[k], a[j]
            k = j
        else:
            break


def heap_sort(a):
    N = len(a)
    aux = [1]
    aux += a
    for k in range(N / 2, 0, -1):
        sink(aux, k, N)
    for k in range(N):
        aux[1], aux[N - k] = aux[N - k], aux[1]
        sink(aux, 1, N - k - 1)

    a[:] = aux[1:]


def test_sort(size, func, is_print=False):
    import numpy as np
    import time
    a = np.random.choice(size, size=size, replace=False)
    a = list(a)
    bg = time.clock()
    func(a)
    print 'time used:{}s'.format(time.clock() - bg)
    if is_print:
        print a


if __name__ == "__main__":
    # test_sort(5000, select_sort)
    # test_sort(5000, insert_sort)
    # test_sort(5000, bubble_sort)
    # test_sort(5000, shell_sort)
    test_sort(50000, merge_sort)
    test_sort(50000, merge_sort_b2u)
    test_sort(50000, quick_sort)
    test_sort(50000, heap_sort)
