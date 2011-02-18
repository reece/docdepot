from __future__ import print_function

import re,os

import Filer
import PubMedArticle
import utils

class FilerAuthor(Filer.Filer):
	rel_dir = 'author'

	def generate_affixes(self,fn,pmid=None):
		if pmid is None:
			pmid = utils.guess_pmid(fn)
			if pmid is None:
				return []
		pma = PubMedArticle.PubMedArticle(pmid)
		ti = pma.title.rstrip('.')
		for au in pma.authors:
			self.logger.debug(au)
		exit
		return map( lambda (au): os.path.join( au, pma.year, ti ),
					pma.authors )


if __name__ == '__main__':
	f = FilerAuthor()
	for fn in Filer.testfiles:
		print('* '+fn)
		print(f.generate_relpaths(fn))
