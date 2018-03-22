#!/usr/bin/env python3
# ECB wrapper skeleton file for 50.020 Security
# Oka, SUTD, 2014
from present import *
import argparse, sys

nokeybits=80
blocksize=64


def ecb(infile,outfile,key,mode):
    """
    Working Version
    """
    if mode.lower()[0] not in 'ed':
        print("Unrecognized cipher mode [Use `ENC`/`DEC`")
        return

    with open(infile, 'rb') as inp_file, open(outfile, 'wb') as out_file:
        while True:
            chunk = inp_file.read(blocksize//8)#.encode('utf-8')
            if chunk:
                chunk_int = int.from_bytes(chunk, byteorder=sys.byteorder)
                if mode.lower()[0] == 'e':
                    # encryption
                    cipher = present(chunk_int, key)
                elif mode.lower()[0] == 'd':
                    # decryption
                    cipher =present_inv(chunk_int, key)
                else:
                    print("Unrecognized cipher mode [Use `ENC`/`DEC`]")
                cipherbytes = cipher.to_bytes(blocksize//8, byteorder=sys.byteorder, signed=False)
                # cipherstring = cipherbytes.decode('utf-8')
                out_file.write(cipherbytes)
            else:
                break


if __name__=="__main__":
    parser=argparse.ArgumentParser(description='Block cipher using ECB mode.')
    parser.add_argument('-i', dest='infile',help='input file')
    parser.add_argument('-o', dest='outfile',help='output file')
    parser.add_argument('-k', dest='keyfile',help='key file')
    parser.add_argument('-m', dest='mode',help='mode')

    args=parser.parse_args()
    infile=args.infile
    outfile=args.outfile
    keyfile=args.keyfile
    mode=args.mode

    with open(keyfile, 'rb') as keyf:
        keys = keyf.read(nokeybits//8)
        key = int.from_bytes(keys, byteorder=sys.byteorder)

    ecb(infile, outfile, key, mode)

