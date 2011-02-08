import hashlib, os

import Filer
import utils

chunksize = 8192						# file read increment

class FilerSHA1(Filer.Filer):
	rel_dir = 'sha1'

	def generate_affixes(self,fn):
		hash = _sha1(fn)
		return [ os.path.join(utils.fn_frag(hash,max_frags=4),hash) ]

def _sha1(fn):
	sha1 = hashlib.sha1()
	with open(fn,'rb') as f: 
		for chunk in iter(lambda: f.read(chunksize), ''):
			sha1.update(chunk)
	return sha1.hexdigest()


if __name__ == '__main__':
	f = FilerSHA1()
	for fn in ['doc/20412080.xml']:
		print fn
		print f.generate_relpaths(fn)

