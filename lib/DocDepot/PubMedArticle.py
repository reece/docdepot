import random
from xml.etree.ElementTree import XML

from Bio import Entrez

rnd = random.random()
Entrez.email = 'reece+%s@berkeley.edu' % rnd
Entrez.tool = '__file__+%s' % rnd


class PubMedArticle:
	def __init__(self,pmid=None):
		if pmid is None:
			raise RuntimeError('must provide a PubMed id')
		self.pmid = pmid
		self.article = __fetch_article(self.pmid)
		
	@property
	def title(self):
		return self.article.find('PubmedArticle/MedlineCitation/Article/ArticleTitle').text

	@property
	def jrnl(self):
		return self.article.find('PubmedArticle/MedlineCitation/Article/Journal/ISOAbbreviation').text

	def __fetch_article(pmid):
		xml = Entrez.efetch(db='nucleotide', id=pmid, retmode='xml').read()
		dom = parseString(xml)
		art = dom.getElementsByTagName('Article')
		return(art)
