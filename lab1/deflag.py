# totally original script
import array, imghdr

def bytecipher_decrypt(bytearr,key):
	decrypt_int = [(i-key) % 256 for i in bytearr]
	decrypted = array.array('B', decrypt_int)
	return decrypted

def get_flagged(bytez):
	for i in range(256):
		cryptheader = bytecipher_decrypt(bytez[:8], i)
		# check for PNG header
		if cryptheader != array.array('B', [137,80,78,71,13,10,26,10]):
			continue
		else:
			print('found!')
			decrypted = bytecipher_decrypt(bytez, i)
			return decrypted
	raise Exception("Might not be a .PNG file")

def doStuff(filein,fileout):
    # open file handles to both files
    with open(filein, mode="rb") as fin:
        with open(fileout, mode='wb') as fout:
        	inputbyte = fin.read()
        	decrypted = get_flagged(inputbyte)
        	fout.write(decrypted)
            

# our main function
if __name__=="__main__":
	doStuff('flag','deflag.png')