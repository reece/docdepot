from __future__ import print_function

import random, sys
import xml.etree.ElementTree as ET

from Bio import Entrez

from memoized import memoized


rnd = random.random()
Entrez.email = 'reecehart+%s@gmail.com' % rnd
Entrez.tool = '__file__+%s' % rnd


class PubMedArticle:
	def __init__(self,pmid=None):
		if pmid is None:
			raise RuntimeError('must provide a PubMed id')
		self.pmid = pmid
		self.art = _fetch_article(self.pmid)

	@property
	def abstract(self):
		return( self._get('Abstract/AbstractText') )

	@property
	def authors(self):
		return( map( _au_to_Last_FM,
					 self.art.findall('AuthorList/Author')))

	@property
	def authors_str(self):
		return( '; '.join(self.authors) )

	@property
	def author1_lastfm(self):
		"""return first author's name, in format LastINITS"""
		au1 = self.art.find('AuthorList/Author')
		return( au1.find('LastName').text + au1.find('Initials').text )

	@property
	def LastFM1(self):
		return self.author1_lastfm

	@property
	def jrnl(self):
		return( self._get('Journal/ISOAbbreviation') )

	@property
	def pages(self):
		return( self._get('Pagination/MedlinePgn') )

	@property
	def title(self):
		return( self._get('ArticleTitle') )

	@property
	def voliss(self):
		ji = self.art.find('Journal/JournalIssue')
		return( '%s(%s)' % (ji.find('Volume').text,ji.find('Issue').text) )

	@property
	def year(self):
		return( self._get('Journal/JournalIssue/PubDate/Year') )
                        



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
	return( au.find('LastName').text + ' ' + au.find('Initials').text )




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