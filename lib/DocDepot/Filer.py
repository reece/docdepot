import os

import utils

class Filer:
	rel_dir = None

	def generate_affixes(self,fn):
		raise Exception('This method should be overridden')

	def generate_relpaths(self,fn):
		ext = os.path.splitext(fn)[1]
		afxs = self.generate_affixes(fn)
		return( map( lambda (a): os.path.join(self.rel_dir,a+ext), afxs ))

	def refile(self,srcfn):
		dsts = self.generate_relpaths(srcfn)
		for dst in dsts:
			#os.makedirs
			#mv/cp/ln/sl
			1+1
		return dsts


if __name__ == '__main__':
	f = Filer('dirA')
	#print f.generate_paths('foo.pdf')

	fn = 'd41d8cd98f00b204e9800998ecf8427e.pdf'
	print fn
	print( "fn_frag(%s): %s" % ('',utils.fn_frag(fn)) )
	for a in [ [2,3], [3,4], [4,2] ]:
		print( "fn_frag(%s): %s" % (a,utils.fn_frag(fn,*a)) )
