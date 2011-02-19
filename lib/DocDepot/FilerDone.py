import hashlib, os

import Filer
import utils

class FilerDone(Filer.Filer):
	rel_dir = 'done'

	def generate_affixes(self,fn):
		return [ os.path.splitext(os.path.basename(fn))[0] ]


if __name__ == '__main__':
	import logging
	logging.basicConfig(level=logging.DEBUG)
	FilerDone().process_incoming(op='nop')
