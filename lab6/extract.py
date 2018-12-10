#!/usr/bin/env python3
# ECB plaintext extraction skeleton file for 50.020 Security
# Oka, SUTD, 2014
import argparse

BLOCKSIZE = 64

def getInfo(headerfile):
    pass

def extract(infile,outfile,headerfile):
    with open(infile, 'rb') as inp_file, \
         open(outfile, 'wb') as out_file, \
         open('fun-'+outfile, 'wb') as outfun_file, \
         open(headerfile, 'r') as hh_file:
        """
        Pardon the nesting T.T
        """
        header = hh_file.read()
        header += '\n'
        print('headerlen', len(header))
        inheader = inp_file.read(len(header))
        out_file.write(header.encode('utf-8'))
        outfun_file.write(header.encode('utf-8'))

        block_freq = {}
        inp_blocks = []

        # frequency analysis
        while True:
            inchunk = inp_file.read(BLOCKSIZE//8)
            if inchunk:
                inp_blocks.append(inchunk)
                block_freq[inchunk] = block_freq.get(inchunk, 0) + 1
            else:
                break

        # for k in block_freq:
        #     print(k, ":", block_freq[k])

        maxfreq = sorted(block_freq.values())[::-1]
        # print(maxfreq)
        mostfreq = [b for b in block_freq if block_freq[b] == maxfreq[0]]
        mostfreq2 = [b for b in block_freq if block_freq[b] == maxfreq[1]]
        mostfreq3 = [b for b in block_freq if block_freq[b] == maxfreq[2]]
        mostfreq4 = [b for b in block_freq if block_freq[b] == maxfreq[3]]
        mostfreq5 = [b for b in block_freq if block_freq[b] == maxfreq[4]]
        mostfreq6 = [b for b in block_freq if block_freq[b] == maxfreq[6]]
        mostfreq7 = [b for b in block_freq if block_freq[b] == maxfreq[7]]
        mostfreq8 = [b for b in block_freq if block_freq[b] == maxfreq[8]]
        mostfreq9 = [b for b in block_freq if block_freq[b] == maxfreq[9]]
        mostfreq10 = [b for b in block_freq if block_freq[b] == maxfreq[10]]
        mostfreq11 = [b for b in block_freq if block_freq[b] == maxfreq[11]]
        mostfreq12 = [b for b in block_freq if block_freq[b] == maxfreq[12]]
        mostfreq13 = [b for b in block_freq if block_freq[b] == maxfreq[13]]
        mostfreq14 = [b for b in block_freq if block_freq[b] == maxfreq[14]]
        mostfreq15 = [b for b in block_freq if block_freq[b] == maxfreq[15]]
        mostfreq16 = [b for b in block_freq if block_freq[b] == maxfreq[16]]
        # print(mostfreq)

        for inpb in inp_blocks:
            if inpb in mostfreq:
                out_file.write(b'00000000') # correct
            else:
                out_file.write(b'11111111') # correct

            # for fun
            if inpb in mostfreq:
                outfun_file.write(b'00000000') # correct
            elif inpb in mostfreq2:
                outfun_file.write(b'11111111') # correct
            elif inpb in mostfreq3:
                outfun_file.write(b'11110000') # shld be correct
            elif inpb in mostfreq4:
                outfun_file.write(b'00000011') # somewhat
            elif inpb in mostfreq5:
                outfun_file.write(b'11111111') # shld be correct
            elif inpb in mostfreq6:
                outfun_file.write(b'00111111') # somewhat
            elif inpb in mostfreq7:
                outfun_file.write(b'11000000') # somewhat
            elif inpb in mostfreq8:
                outfun_file.write(b'00001111') # shld be correct
            elif inpb in mostfreq9:
                outfun_file.write(b'11111100') # shld be correct
            elif inpb in mostfreq10:
                outfun_file.write(b'00011111') # shld be correct
            elif inpb in mostfreq11:
                outfun_file.write(b'11111000') # shld be correct
            elif inpb in mostfreq12:
                outfun_file.write(b'01111111') # shld be correct
            elif inpb in mostfreq13:
                outfun_file.write(b'11100000') # shld be correct
            elif inpb in mostfreq14:
                outfun_file.write(b'11100000') # shld be correct
            elif inpb in mostfreq15:
                outfun_file.write(b'00111111') # correct
            elif inpb in mostfreq16:
                outfun_file.write(b'00000111') # correct
            else:
                outfun_file.write(b'11111111')

if __name__=="__main__":
    parser=argparse.ArgumentParser(description='Extract PBM pattern.')
    parser.add_argument('-i', dest='infile',help='input file, PBM encrypted format')
    parser.add_argument('-o', dest='outfile',help='output PBM file')
    parser.add_argument('-hh', dest='headerfile',help='known header file')

    args=parser.parse_args()
    infile=args.infile
    outfile=args.outfile
    headerfile=args.headerfile

    print('Reading from: %s'%infile)
    print('Reading header file from: %s'%headerfile)
    print('Writing to: %s'%outfile)

    success=extract(infile,outfile,headerfile)

            
