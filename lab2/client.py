#!/usr/bin/python3
# -*- coding: utf-8 -*-
# DA+Nils 2018

"""
Lab2: Breaking Ciphers

Pwntool client for python3

Install: see install.sh

Documentation: https://python3-pwntools.readthedocs.io/en/latest/
"""

from pwn import remote

# pass two bytestrings to this function
def XOR(a, b):
    r = b''
    for x, y in zip(a, b):
        r += (x ^ y).to_bytes(1, 'big')
    return r

def get_chara_freq(message):
    msg = str(message)
    freq = {}
    for char in msg:
        if char not in freq:
            freq[char] = 0
        freq[char] += 1

    sorted_ = "a"
    for char in freq:
        if char == 'a':
            continue

        for i in range(len(sorted_)):
            if freq[char] >= freq[sorted_[i]]:
                sorted_ = sorted_[:i] + char + sorted_[i:]
                break

        if char not in sorted_:
            sorted_ += char
    # print(sorted_)
    return sorted_

def get_sherlock_freq():
    with open('sherlock.txt', 'r') as sherlock:
        return get_chara_freq(''.join(sherlock.read().split('\r')))

def get_mapping(text1, text2):
    if len(text1) != len(text2):
        print("WARNING: DIFFERENT LENGTH ", len(text1), len(text2))
    charmap = {text1[i]:text2[i]
                for i in range(min(len(text1),
                                   len(text2)))}
    print(charmap)
    return charmap

def get_hardcoded_swapmap():
    swapmap = {char:char for char in get_sherlock_freq()}

    # ----
    swapmap['s'] = 'i' #addressed
    swapmap['d'] = 's' #addressed
    swapmap['r'] = 'd' #addressed
    swapmap['o'] = 'a' 
    swapmap['a'] = 'o' #not addressed
    swapmap['u'] = 'w' #not addressed
    swapmap['w'] = 'u' #not addressed
    swapmap['n'] = 'h' #addressed
    swapmap['h'] = 'r' #addressed
    swapmap['g'] = 'y' #addressed
    swapmap['i'] = 'n' #addressed
    swapmap['I'] = 'v'
    swapmap['m'] = 'g'
    swapmap['y'] = 'm'
    swapmap['f'] = 'c'
    swapmap[','] = 'p'
    swapmap['"'] = 'b'
    swapmap['p'] = 'f'
    swapmap['c'] = ','
    swapmap['v'] = 'k'
    swapmap['W'] = 'q'
    swapmap['T'] = "'"
    swapmap['H'] = ' '
    swapmap['-'] = 'j'
    swapmap['k'] = '"'
    swapmap['S'] = '?'

    return swapmap


 
def map_message(message):
    msg = ''.join(str(message).split())
    msg_srt = get_chara_freq(msg)
    mapp = get_mapping(msg_srt, get_sherlock_freq())
    
    swapmap = get_hardcoded_swapmap()
    
    out = ''.join([mapp[i] for i in msg[1:-1]])

    #clearing b
    out_nb = ''.join(out.split('b'))

    out = ''.join([swapmap[i] for i in out_nb])

    out = '\t' + out
    return out

def sol1():
    conn = remote(URL, PORT)
    message = conn.recvuntil('-Pad')  # receive TCP stream until end of menu
    conn.sendline("1")  # select challenge 1

    dontcare = conn.recvuntil(':')
    challenge = conn.recvline()
    # print(challenge)
    # get_chara_freq(challenge)
    result = map_message(challenge)
    print(result)
    # decrypt the challenge here
    solution = (0).to_bytes(7408, byteorder='big')
    conn.send(solution)
    message = conn.recvline()
    message = conn.recvline()
    if b'Congratulations' in message:
        print(message)
    conn.close()


def sol2():
    conn = remote(URL, PORT)
    message = conn.recvuntil('-Pad')  # receive TCP stream until end of menu
    conn.sendline("2")  # select challenge 2

    dontcare = conn.recvuntil(':')
    challenge = conn.recvline()
    # some all zero mask.
    # TODO: find the magic mask!
    mask = (0).to_bytes(len(message), 'big')
    message = XOR(challenge, mask)
    conn.send(message)
    message = conn.recvline()
    message = conn.recvline()
    if b'exact' in message:
        print(message)
    conn.close()


if __name__ == "__main__":

    # NOTE: UPPERCASE names for constants is a (nice) Python convention
    URL = 'scy-phy.net'
    PORT = 1337

    sol1()
    sol2()
