# Create your views here.

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.template import Context
from django.template.loader import get_template

import os, sys
sys.path += [os.path.join(
	os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))),
	'lib'
	)]
from DocDepot.PubMedArticle import PubMedArticle


@login_required
def pubmed(request):
	template = get_template('pubmed.html')
	pmid = request.META['QUERY_STRING']
	if pmid:
		pma = PubMedArticle(pmid)
	variables = Context({
		'page_title': 'PubMed Lookup',
		'pmid': pmid,
		'pma': pma,
		'user': request.user,
		})
	output = template.render(variables)
	return HttpResponse(output)

