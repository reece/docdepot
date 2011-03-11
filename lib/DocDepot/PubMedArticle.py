from __future__ import print_function

import logging, pprint, random, sys
import xml.etree.ElementTree as ET

from Bio import Entrez

from memoized import memoized

logger = logging.getLogger(__package__)

rnd = random.random()
Entrez.email = 'reecehart+%s@gmail.com' % rnd
Entrez.tool = '__file__+%s' % rnd


class PubMedArticle:
	def __init__(self,pmid=None):
		if pmid is None:
			raise RuntimeError('must provide a PubMed id')
		self.pmid = pmid
		self.art = _fetch_article(self.pmid)
		if self.art is None:
			raise Exception("Couldn't find PubMed info for pmid:"+pmid)

	@property
	def abstract(self):
		return( self._get('Abstract/AbstractText') )

	@property
	# N.B. Citations may have 0 authors. e.g., pmid:7550356
	def authors(self):
		authors = [ _au_to_Last_FM(au) for au in self.art.findall('AuthorList/Author') ]
		return authors

	@property
	def authors_str(self):
		return( '; '.join(self.authors) )

	@property
	def author1_LastFM(self):
		"""return first author's name, in format LastINITS"""
		au1 = _au_to_Last_FM(self.art.find('AuthorList/Author'))
		return au1

	@property
	def jrnl(self):
		j = self._get('Journal/ISOAbbreviation')
		if j is None:
			# e.g., http://www.ncbi.nlm.nih.gov/pubmed?term=21242195
			j = self._get('Journal/Title')
		assert j is not None
		return j

	@property
	def pages(self):
		return( self._get('Pagination/MedlinePgn') )

	@property
	def title(self):
		return( self._get('ArticleTitle') )

	@property
	def voliss(self):
		ji = self.art.find('Journal/JournalIssue')
		try:
			return( '%s(%s)' % (ji.find('Volume').text,
								ji.find('Issue').text) )
		except AttributeError:
			pass
		try:
			return( ji.find('Volume').text )
		except AttributeError:
			pass
		# electronic pubs may not have volume or issue
		# e.g., http://www.ncbi.nlm.nih.gov/pubmed?term=20860988
		logger.info("No volume for "+self.pmid)
		return None

	@property
	def year(self):
		y = self._get('Journal/JournalIssue/PubDate/Year')
		if y is None:
			# case applicable for pmid:9887384 (at least)
			y = self._get('Journal/JournalIssue/PubDate/MedlineDate')[0:4]
		assert y is not None
		return y

	def _get(self,tag):
		n = self.art.find(tag)
		if n is not None:
			return n.text
		return None
	
	def __str__(self):
		return( '%s (%s. %s, %s:%s)'.format(
			self.title, self.authors_str, self.jrnl, self.voliss, self.pages) )
		



############################################################################
## Utilities

@memoized
def _fetch_article(pmid):
	xml = Entrez.efetch(db='pubmed', id=pmid, retmode='xml').read()
	art = ET.fromstring(xml).find('PubmedArticle/MedlineCitation/Article')
	#testing: art = ET.parse('doc/20412080.xml').find('PubmedArticle/MedlineCitation/Article')
	return art

def _au_to_Last_FM(au):
	if au is None:
		return
	try:
		return( au.find('LastName').text
				+ u' ' + au.find('Initials').text )
	except AttributeError:
		pass
	try:
		return( au.find('CollectiveName').text )
	except AttributeError:
		pass
	try:
		return( au.find('LastName').text )
	except AttributeError:
		pass
	raise Exception("Author structure not recognized")


# This helps debug:
# curl 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=19483685'



if __name__ == '__main__':
	a = PubMedArticle(20412080)
	print( a.art )
	print( a.title )
	print( a.authors_str )
	print( a.jrnl )
	print( a.voliss )
	print( a.pages )
	print( a.year )
	print( a.LastFM1 )

	a = PubMedArticle(20412080)
	print( a.year )
