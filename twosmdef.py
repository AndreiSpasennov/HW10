def find_two_smallest(a):
    min1 = min(a)
    min2 = min(v for v in a if v != min1)
    return (min1, min2)