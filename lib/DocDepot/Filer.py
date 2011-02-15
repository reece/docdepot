from __future__ import print_function

import logging, os, random, shutil, string, sys

import utils

testfiles = [ '20412080.xml', 'doc/20412080.xml', 'bogus.pdf', __file__ ]

class Filer:
	# TODO: top_dir path is defined here and in urls.py document_root
	top_dir = '/srv/locuslibrary/files'
	in_dir = 'incoming'
	err_dir = 'errors'
	rel_dir = None
	ops = {
		'cp': shutil.copyfile,
		'mv': shutil.move,
		'ln': os.link,
		'sl': lambda (src,dst): os.symlink(os.path.relpath(src,dst),dst)
		}

	def generate_affixes(self,fn):
		raise Exception('This method should be overridden by subclasses')

	def generate_relpaths(self,fn):
		ext = os.path.splitext(fn)[1]
		afxs = self.generate_affixes(fn)
		return( map( lambda (a): os.path.join(self.rel_dir,a+ext), afxs ))

	def refile(self,src,op='ln',dsts=None):
		if dsts is None:
			dsts = map( lambda (rp): os.path.join(self.top_dir,rp),
						self.generate_relpaths(src) )
		for dst in dsts:
			dstp = os.path.dirname(dst)
			if not os.path.exists(dstp):
				os.makedirs(dstp)
			try:
				self.ops[op](src,dst)
			except OSError as e:
				raise OSError('%s(%s,%s) failed: %s' % (op,src,dst,e))
			print( '%s(%s,%s)' % (op,src,dst) );
		return dsts

	def process_incoming(self):
		in_path = os.path.join(self.top_dir, self.in_dir)
		for bn in os.listdir(in_path):
			src = os.path.join(in_path,bn)
			try:
				self.refile(src)
				os.remove(src)
			except Exception as e:
				print(e,file=sys.stderr) # TODO: use logging
				self.refile_error(src)
				
	def refile_error(self,src):
		try:
			self.refile(src,op='mv',
				dsts=[os.path.join(self.top_dir,self.err_dir,
								   os.path.basename(src)+'-'+_random_string())])
		except Exception as e:
			print(e,file=sys.stderr) # TODO: use logging
			

def _random_string(N=6):
	return ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(N))
