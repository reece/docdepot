import hashlib, os

import Filer

chunksize = 8192						# file read increment

class FilerSHA1(Filer.Filer):
	def generate_affixes(self,fn):
		hash = _sha1(fn)
		return( [os.path.join(_hashpath(hash),hash)] )

def _sha1(fn):
	sha1 = hashlib.sha1()
	with open(fn,'rb') as f: 
		for chunk in iter(lambda: f.read(chunksize), ''):
			sha1.update(chunk)
	return sha1.hexdigest()

def _hashpath(hash):
	return os.path.join(hash[0:2],hash[2:4],hash[4:6])

if __name__ == '__main__':
	f = FilerSHA1('dirA')
	print f.generate_affixes(__file__)
	print f.generate_paths(__file__)

