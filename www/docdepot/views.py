# Create your views here.

from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template

def pubmed(request):
	template = get_template('pubmed.html')
	variables = Context({
		'page_title': 'PubMed Lookup',
		})
	output = template.render(variables)
	return HttpResponse(output)

