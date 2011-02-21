# Create your views here.

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.template import Context
from django.template.loader import get_template

import os, sys
sys.path += [os.path.join(
	os.path.dirname(os.path.dirname(os.path.dirname(
		os.path.realpath(__file__)))),
	'lib'
	)]
from DocDepot.PubMedArticle import PubMedArticle
from DocDepot.FilerPMID import FilerPMID


#@login_required
def pubmed(request):
	pma = None
	error = None
	pmid = request.META['QUERY_STRING']
	q_id = request.GET.get('id')
	if q_id is not None and q_id[0:5] == 'pmid:':
		pmid = q_id[5:]
	if pmid:
		try:
			pma = PubMedArticle(pmid)
		except Exception as e:
			pass
	variables = Context({
		'title': 'PubMed Lookup',
		'pmid': pmid,
		'pma': pma,
		'user': request.user,
		'rp': FilerPMID().pmid_pdf_exists(pmid),
		})
	output = get_template('pubmed.html').render(variables)
	return HttpResponse(output)


def help(request):
	variables = Context({
		'title': 'Help',
		})
	output = get_template('help.html').render(variables)
	return HttpResponse(output)
