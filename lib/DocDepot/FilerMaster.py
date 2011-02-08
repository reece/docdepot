import Filer
import FilerSHA1
import FilerPMID
import FilerLocus


class FilerMaster(Filer.Filer):
	def __init__(self):
		self.locusfiler = FilerLocus.FilerLocus()
		self.pmidfiler = FilerPMID.FilerPMID()
		self.sha1filer = FilerSHA1.FilerSHA1()

	def generate_relpaths(self,fn):
		return(
			self.locusfiler.generate_relpaths(fn),
			self.pmidfiler.generate_relpaths(fn),
			self.sha1filer.generate_relpaths(fn)
			)


if __name__ == '__main__':
	f = FilerMaster()
	fn = 'doc/20412080.xml'
	print fn
	print f.generate_relpaths(fn)
	
