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
		afxs = map( lambda (au): os.path.join(au,u'%s (%s) %s' % (pma.year,pma.jrnl,ti)),
					pma.authors )
		return afxs


if __name__ == '__main__':
	import logging
	logging.basicConfig(level=logging.DEBUG)
	FilerAuthor().process_incoming(op='nop')
