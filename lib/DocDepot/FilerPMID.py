from __future__ import print_function

import re

import Filer
import utils

class FilerPMID(Filer.Filer):
	rel_dir = 'pmid'

	def generate_affixes(self,fn,pmid=None):
		if pmid is None:
			pmid = utils.guess_pmid(fn)
		if pmid is not None:
			return [pmid]
		return ()

if __name__ == '__main__':
	f = FilerPMID()
	for fn in Filer.testfiles:
		print( '* '+fn )
		print( f.generate_relpaths(fn) )
