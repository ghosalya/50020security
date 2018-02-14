import hashlib
import timeit
import random
from itertools import permutations, product
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
        charset = 'abcdefghijklmnopqrstuvwxyz0123456789'
        perms = [''.join(p) for p in product(charset, repeat=5)]
        for p in perms:
            hassh = hash_(p)
            if hassh in hashes:
                mapped_hash.update({p: hassh})
    return mapped_hash

def salt_passwords(mapped_hash):
    salted_pass = [pas+random.choice('abcdefghijklmnopqrstuvwxyz')
                   for pas in mapped_hash]

    with open('pass6.temp.txt', 'w') as p6:
        with open('salted6.temp.txt', 'w') as sp6:
            # temp is used in file name to avoid
            # overriding the original files (that is used in the report)
            for pas in salted_pass:
                p6.write(pas+'\n')
                sp6.write(hash_(pas)+'\n')


if __name__ == '__main__':

    start = datetime.now()
    hashed = get_hash()
    end = datetime.now()
    print("Time:",end-start)

    for k in hashed:
        print(k, hashed[k])

    # comment if dont want to generate new salt
    # salt_passwords(hashed)


    # tmit = timeit.timeit('get_hash()', 
    #               setup='from __main__ import get_hash', 
    #               number=10)
    # print(tmit)
