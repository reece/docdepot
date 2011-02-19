from __future__ import print_function

import filecmp, logging, os, shutil, stat, sys
import utils

#TODO: on collision, gen unique name

class Filer:
	#top_path = '/srv/locuslibrary'
	top_path = '/srv/locuslibrary/docdepot'
	files_dir = 'files'
	files_path = os.path.join(top_path, files_dir)
	in_dir = 'incoming'
	err_dir = 'errors'
	rel_dir = None
	dir_mode = 02775					# 02775 = rwxrwsr-x
	logger = logging.getLogger(__package__)
	ops = {
		'cp': shutil.copyfile,
		'mv': shutil.move,				# TODO: drop this; too unlike cp/ln/sl
		'ln': os.link,
		'sl': lambda src,dst: os.symlink(os.path.relpath(src,dst),dst),
		'nop': lambda src,dst: 0
		}

	def generate_affixes(self,fn):
		raise Exception('This method should be overridden by subclasses')

	def generate_relpaths(self,fn):
		ext = os.path.splitext(fn)[1]
		afxs = self.generate_affixes(fn)
		return( map( lambda (a): os.path.join(self.rel_dir,a+ext), afxs ))

	def process_incoming(self,op='ln'):
		in_rp = os.path.join(self.files_path, self.in_dir)
		for bn in os.listdir(in_rp):
			src = os.path.join(in_rp,bn)
			self.logger.debug('processing '+src)
			try:
				dsts = map( lambda (rp): os.path.join(self.files_path,rp),
							self.generate_relpaths(src) )
				self.refile(src,dsts,op=op)
				os.remove(src)			# TODO: Leave this to the caller
			except Exception as e:
				self.logger.error(e)
				self.refile_error(src)

	def refile(self,src,dsts,op='ln'):
		for dst in dsts:
			#  handle cases when dst exists
			if os.path.exists(dst):
				if (os.path.samefile(src,dst)
					or filecmp.cmp(src,dst,shallow=False)):
					# file is identical (same inode) or same content;
					# either way, we remove the src if the original op
					# would have also removed the src.
					if op in ['mv']:
						os.remove(src)
						self.logger.info('removed src file; same-named destination with same content already exists')
					continue
				else:
					# dst exists, but isn't same inode or content
					# Although there's a potential very rare race here,
					# we'll catch with exceptions
					dst = utils.next_version(dst)
			
			# make the directory path
			dstp = os.path.dirname(dst)
			if not os.path.exists(dstp):
				# N.B. makedirs(mode=) is subject to umask
				# easier to set explicitly
				os.makedirs(dstp)
				os.chmod(dstp,self.dir_mode)
			
			try:
				self.ops[op](src,dst)
			except OSError as e:
				raise OSError('%s(%s,%s): failure: %s' % (op,src,dst,e))
			self.logger.info( '%s(%s,%s): success' % (op,src,dst) );
		return dsts

	def refile_error(self,src):
		# TODO: errors should be an Filer
		root,ext = os.path.splitext(src)
		dst = os.path.join( self.files_path,
							self.err_dir,
							os.path.basename(src) )
		if os.path.exists(dst):
			dst = utils.unique_name(dst)
		try:
			self.refile(src,dsts=[dst],op='mv')
		except Exception as e:
			self.logger.error(e)
