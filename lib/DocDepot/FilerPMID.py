import re

import Filer
import utils

class FilerPMID(Filer.Filer):
	rel_dir = 'pmid'

	def generate_affixes(self,fn,pmid=None):
		if pmid is None:
			pmid = utils.guess_pmid(fn)
			if pmid is None:
				raise Exception("Couldn't infer pmid from %s" % (fn))
		return [pmid]


if __name__ == '__main__':
	f = FilerPMID()
	x = '20412080.pdf'
	print(x)
	print('guess_pmid: %s' % (_guess_pmid(x)))
	print(f.generate_relpaths(x))
