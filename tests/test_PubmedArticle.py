#!/usr/bin/python

import os, pprint, sys

sys.path += [os.path.join(
	os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
	'lib'
	)]

from DocDepot import PubmedArticle

a = PubmedArticle(20412080)

pprint.pprint(a)
