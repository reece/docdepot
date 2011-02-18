from __future__ import print_function

import os,re

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

	def pmid_pdf_exists(self,pmid):
		rp = os.path.join(self.rel_dir, pmid+'.pdf')
		if os.path.exists(os.path.join(self.files_path, rp)):
			return rp
		return None

if __name__ == '__main__':
	f = FilerPMID()
	for fn in Filer.testfiles:
		print( '* '+fn )
		print( f.generate_relpaths(fn) )
