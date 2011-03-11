from __future__ import print_function

import re,os

import Filer
import PubMedArticle
import utils

import logging
logging.basicConfig(level=logging.DEBUG)

class FilerJournal(Filer.Filer):
	rel_dir = 'journal'

	def generate_affixes(self,fn,pmid=None):
		if pmid is None:
			pmid = utils.guess_pmid(fn)
			if pmid is None:
				return []
		pma = PubMedArticle.PubMedArticle(pmid)
		ti = utils.elide_string(pma.title.rstrip('.'),max_len=150)
		y = pma.year
		if y is None:
			y = u''
		vi = pma.voliss
		if vi is None:
			vi = u''
		au1 = pma.author1_LastFM
		if au1 is None:
			au1 = u''
		afxs = os.path.join( pma.jrnl, y, vi, u'%s: %s' % (au1,ti) )
		return [ afxs ]


if __name__ == '__main__':
	import logging
	logging.basicConfig(level=logging.DEBUG)
	FilerJournal().process_incoming(op='nop')
