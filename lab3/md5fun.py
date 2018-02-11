import hashlib
import timeit
from itertools import permutations
from datetime import datetime


def hash_(word):
    m = hashlib.md5()
    m.update(word.encode())
    return m.hexdigest()

def get_hash():
    hashes = []
    mapped_hash = {}

    with open('hash5.txt', 'r') as hh:
        hashes = [h.strip() for h in hh]

    with open('words5.txt', 'r') as w5:
        for word in w5:
            perms = [''.join(p) for p in permutations(word.strip())]
            for p in perms:
                perm_n = [p]
                for i in range(5):
                    n_perm = []
                    for j in '0123456789':
                        n_perm += [pp[:i]+j+p[i:] for pp in perm_n]
                        # print(n_perm)
                    perm_n += n_perm
                mapped_hash.update({w: hash_(w) for w in perm_n 
                                    if hash_(w) in hashes})
    return mapped_hash


if __name__ == '__main__':

    start = datetime.now()
    hashed = get_hash()
    end = datetime.now()
    print("Time:",end-start)

    for k in hashed:
        print(k, hashed[k])
    # tmit = timeit.timeit('get_hash()', 
    #               setup='from __main__ import get_hash', 
    #               number=10)
    # print(tmit)
