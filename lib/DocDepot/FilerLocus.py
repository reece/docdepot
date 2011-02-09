from __future__ import print_function

import Filer
import PubMedArticle
import utils

class FilerLocus(Filer.Filer):
	rel_dir = 'locus'

	def generate_affixes(self,fn,pmid=None):
		if pmid is None:
			pmid = utils.guess_pmid(fn)
			if pmid is None:
				return []
		pma = PubMedArticle.PubMedArticle(pmid)
		if pma is None:
			raise Exception("Couldn't find PubMed id %s" % (pmid))
		return ['{0.pmid}_{0.year}_{0.jrnl}_{0.LastFM1}'.format(pma)]


if __name__ == '__main__':
	f = FilerLocus()
	for fn in Filer.testfiles:
		print( '* ' + fn)
		print( f.generate_relpaths(fn) )
