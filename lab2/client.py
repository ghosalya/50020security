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
from array import array

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

def get_abstract_freq():
    abstracts = [' ','e','t','a','o','h','r','n','d','i',
                 's','l','w','\n','g',',','u','c','m', 'y',
                 'f','p','.','b','k','v','\"','-','\'','j',
                 'q','?',"\t","+"]
    return abstracts

def get_mapping(text1, text2):
    if len(text1) != len(text2):
        print("WARNING: DIFFERENT LENGTH ", len(text1), len(text2))
    charmap = {text1[i]:text2[i]
                for i in range(min(len(text1),
                                   len(text2)))}
    # print(charmap)
    return charmap

def get_hardcoded_swapmap():
    swapmap = {char:char for char in get_abstract_freq()}

    # ----
    swapmap['"'] = 'v'
    swapmap['v'] = '"'
    # ----
    swapmap['?'] = "q"
    swapmap['q'] = "?"
    # ----
    swapmap['j'] = "'"
    swapmap["'"] = "j"

    return swapmap


def map_message(message):
    msg = ''.join([chr(byte) for byte in message if byte != b'r'])
    msg_srt = get_chara_freq(msg)
    mapp = get_mapping(msg_srt, get_abstract_freq())
    swapmap = get_hardcoded_swapmap()

    out_a = [mapp[i] for i in msg[1:-1] if i in mapp]
    out_b = [swapmap[i] for i in out_a]
    
    out = "\t" + ''.join(out_b)
    # print('LENGTH:', len(out))

    return out

def sol1():
    conn = remote(URL, PORT)
    message = conn.recvuntil('-Pad')  # receive TCP stream until end of menu
    conn.sendline("1")  # select challenge 1

    dontcare = conn.recvuntil(':')
    challenge = conn.recvline()

    # decrypt the challenge here
    result = map_message(challenge)
    solution = result.encode()

    message = conn.recvline()
    conn.send(solution)
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
    incoming = 'Submitted student ID: 1000000 and grade 0. [<-- this is not the exact plaintext]\n'
    inco_byte = incoming.encode()
    print(inco_byte)
    target = 'Submitted student ID: 1001841 and grade 4. [<-- this is not the exact plaintext]\n'
    targ_byte = target.encode()
    print(targ_byte)
    # TODO: find the magic mask!
    # mask = (400).to_bytes(len(message), 'big')
    mask = XOR(inco_byte, targ_byte)
    print(mask)
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

    # sol1()
    sol2()
