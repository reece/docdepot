import re

import Filer
import PubMedArticle

class FilerPubMed(Filer.Filer):
	def generate_affixes(self,fn,pmid=None):
		if pmid is None:
			pmid = _guess_pmid(fn)
			if pmid is None:
				raise Exception("Couldn't infer pmid from %s" % (fn))
		pma = PubMedArticle(pmid)
		


def _guess_pmid(fn):
	m = re.match( '(\d+)[_\.]', fn )
	if m:
		return m.group(1)
	return None


if __name__ == '__main__':
	x = '20412080.pdf'
	print( '%s -> %s' % (x, _guess_pmid(x)) )
	
	
