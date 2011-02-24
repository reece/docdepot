from __future__ import print_function

import Filer
import FilerAuthor
import FilerJournal
import FilerLocus
import FilerPMID
import FilerSHA1

class FilerMaster(Filer.Filer):
	def __init__(self):
		self.aufiler = FilerAuthor.FilerAuthor()
		self.jrnlfiler = FilerJournal.FilerJournal()
		self.locusfiler = FilerLocus.FilerLocus()
		self.pmidfiler = FilerPMID.FilerPMID()
		self.sha1filer = FilerSHA1.FilerSHA1()

	def generate_relpaths(self,fn):
		return(
			self.aufiler.generate_relpaths(fn)
			+ self.jrnlfiler.generate_relpaths(fn)
			+ self.locusfiler.generate_relpaths(fn)
			+ self.pmidfiler.generate_relpaths(fn)
			+ self.sha1filer.generate_relpaths(fn)
			)

		


if __name__ == '__main__':
	f = FilerMaster()
	f.process_incoming()
