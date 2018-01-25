#!/usr/bin/env python3
# SUTD 50.020 Security Lab 1
# Simple file read in/out
# Quyen, 2014

# Import libraries
import sys, string
import argparse

rev_printable = {string.printable[i]:i for i in range(len(string.printable))}

def shift_right(text, key):
    text_ord = [rev_printable[i] for i in text]
    text_crypt = [string.printable[(i+key)%100] for i in text_ord]
    cryptext = ''.join(text_crypt)
    return cryptext

def shift_left(text, key):
    return shift_right(text, key*-1)

def doStuff(filein,fileout, key, mode):
    # open file handles to both files
    with open(filein, mode="r", encoding='utf-8', newline='\n') as fin:
        with open(fileout, mode='w', encoding='utf-8', newline='\n') as fout:
            c    = fin.read()         # read in file into c as a str
            # and write to fileout
            if mode=="e":
                cryptext = shift_right(c, key)
            elif mode=="d":
                cryptext = shift_left(c, key)

            fout.write(cryptext)
            

# our main function
if __name__=="__main__":
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='filein',help='input file', required=True)
    parser.add_argument('-o', dest='fileout', help='output file', required=True)
    parser.add_argument('-k', dest='key', help='integer key to shift by',
                                          type=int, default=0)
    parser.add_argument('-m', dest='mode', 
                        help='"e" for encryption, "d" for decryption',
                        default="e")


    # parse our arguments
    args = parser.parse_args()
    filein = args.filein
    fileout = args.fileout
    key = args.key
    mode = args.mode.lower()

    if key not in range(256):
        raise ValueError('Key must be between 0-255 inclusive')

    if mode not in 'ed':
        raise Exception('Mode must be either [e]ncrypt or [d]ecrypt')        

    doStuff(filein,fileout, key, mode)

    # all done


