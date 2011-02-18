from __future__ import print_function

import logging, os, random, shutil, stat, string, sys
import utils

testfiles = [ '20412080.xml', 'doc/20412080.xml', 'bogus.pdf', __file__ ]

class Filer:
	top_path = '/srv/locuslibrary'
	files_dir = 'files'
	files_path = os.path.join(top_path, files_dir)
	in_dir = 'incoming'
	err_dir = 'errors'
	rel_dir = None
	dir_mode = 02775					# 02775 = rwxrwsr-x
	logger = logging.getLogger(__package__)
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

	def process_incoming(self):
		in_rp = os.path.join(self.files_path, self.in_dir)
		for bn in os.listdir(in_rp):
			src = os.path.join(in_rp,bn)
			self.logger.debug('processing '+src)
			dsts = map( lambda (rp): os.path.join(self.files_path,rp),
						self.generate_relpaths(src) )
			try:
				self.refile(src,dsts)
				os.remove(src)
			except Exception as e:
				self.logger.error(e)
				self.refile_error(src)
			exit

	def refile(self,src,dsts,op='ln'):
		for dst in dsts:
			dstp = os.path.dirname(dst)
			if not os.path.exists(dstp):
				os.makedirs(dstp)
				os.chmod(dstp,self.dir_mode)
			try:
				self.ops[op](src,dst)
			except OSError as e:
				raise OSError('%s(%s,%s) failed: %s' % (op,src,dst,e))
			self.logger.info( '%s(%s,%s)' % (op,src,dst) );
		return dsts

	def refile_error(self,src):
		def _random_string(N=6):
			return ''.join(random.choice(
				string.ascii_lowercase + string.digits) for x in range(N))
		root,ext = os.path.splitext(src)
		dst = os.path.join( self.files_path,
							self.err_dir,
							os.path.basename(src) )
		if os.path.exists(dst):
			dst = os.path.join( self.files_path,
								self.err_dir,
								os.path.basename(root)+'-'+_random_string()+ext )
		try:
			self.refile(src,dsts=[dst],op='mv')
		except Exception as e:
			self.logger.error(e)
