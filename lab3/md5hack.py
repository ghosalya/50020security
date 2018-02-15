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

    with open('hash_clear.txt', 'r') as hh:
        hashes = [h.strip() for h in hh]
        charset = 'abcdefghijklmnopqrstuvwxyz0123456789@'
        perms = [''.join(p) for p in product(charset, repeat=9)]
        for p in perms:
            hassh = hash_(p)
            if hassh in hashes:
                mapped_hash.update({p: hassh})
    return mapped_hash

def get_english_hash():
    hashes = []
    mapped_hash = {}

    with open('hash_clear.txt', 'r') as hh:
        hashes = [h.strip() for h in hh]
        charset = 'abcdefghijklmnopqrstuvwxyz0123456789@'
        with open('american-english','r') as ae:
            for line in ae:
                pp = line.strip()#.split()[1]

                p = pp
                hassh = hash_(p)
                if hassh in hashes:
                    mapped_hash.update({p: hassh})

                # p = pp.title()
                # hassh = hash_(p)
                # if hassh in hashes:
                #     mapped_hash.update({p: hassh})

                p = pp.upper()
                hassh = hash_(p)
                if hassh in hashes:
                    mapped_hash.update({p: hassh})
                
                p = pp+'123'
                hassh = hash_(p)
                if hassh in hashes:
                    mapped_hash.update({p: hassh})

                p = pp.title()+'123'
                hassh = hash_(p)
                if hassh in hashes:
                    mapped_hash.update({p: hassh})

                p = pp+'s'
                hassh = hash_(p)
                if hassh in hashes:
                    mapped_hash.update({p: hassh})
    return mapped_hash


if __name__ == '__main__':

    start = datetime.now()
    hashed = get_english_hash()
    end = datetime.now()
    print("Time:",end-start)
    print("Found", len(hashed),'hashes:')
    for k in hashed:
        print(k, hashed[k])

    # tmit = timeit.timeit('get_hash()', 
    #               setup='from __main__ import get_hash', 
    #               number=10)
    # print(tmit)

# using english dictionary (/usr/share/dict/american-english)
# dict file provided just in case
#
# Time: 0:00:04.492409
# Found 15 hashes:
# Cara123 f46565ba900fb8fb166521bd4bb6e2e7
# banana 72b302bf297a228a75730123efef7c41
# cats 0832c1202da8d382318e329a7c133ea0
# donkey 9443b0fceb8c03b6a514a706ea69df0b
# dragon 8621ffdbc5698829397d97767ac13db3
# hello123 f30aa7a662c728b7407c54ae6bfd27d1
# kamikaze123 b419e81184e9492a74d9646e23ebc82d
# orange fe01d67a002dfa0f3ac084298142eccd
# password 5f4dcc3b5aa765d61d8327deb882cf99
# password123 482c811da5d5b4bc6d497ffa98491e38
# secret 5ebe2294ecd0e0f08eab7690d2a6ee69
# sheep 23ec24c5ca59000543cee1dfded0cbea
# skeleton 84df077bcb1bd39ab1a3294de0cf655b
# television 79464212afb7fd6c38699d0617eaedeb
# treasure 82210e61e8f415525262575b20fae48d