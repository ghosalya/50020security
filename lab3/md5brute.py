import hashlib
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
        charset = 'abcdefghijklmnopqrstuvwxyz0123456789'
        perms = [''.join(p) for p in permutations(charset, 5)]
        for p in perms:
            mapped_hash.update({w: hash_(w) for w in perms 
                                if hash_(w) in hashes})
    return mapped_hash



if __name__ == '__main__':

    start = datetime.now()
    hashed = get_hash()
    end = datetime.now()
    print("Time:",end-start)

    for k in hashed:
        print(k, hashed[k])