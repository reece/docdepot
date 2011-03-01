from __future__ import print_function

import filecmp, logging, os, shutil, stat, sys
import utils

#TODO: on collision, gen unique name

# Current structure of the destination path:
# dst = top_path / rel_dir / affix+ext
# Filers define rel_dir and an generator for affix(es)
# This class does the rest to build the path and refile
# Currently, affixes are suffixless.  This class adds the suffix back.
# This extension handling is a think-o that could be fixed.

class Filer:
	#top_path = '/srv/locuslibrary/docdepot'   # testing
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
		'mv': shutil.move,				# TODO: drop this; too unlike cp/ln/sl
		'ln': os.link,
		'sl': lambda src,dst: os.symlink(os.path.relpath(src,dst),dst),
		'nop': lambda src,dst: 0
		}

	def generate_affixes(self,fn):
		# TODO: g_a expects extension-less paths. This was originally done
		# so that all files would have the same suffix. That's lame. Just
		# return the full relpath, with extension (if any)
		raise Exception('This method should be overridden by subclasses')

	def generate_relpaths(self,fn):
		ext = os.path.splitext(fn)[1]
		afxs = self.generate_affixes(fn)
		return( map( lambda (a): os.path.join(self.rel_dir,a+ext), afxs ))

	def generate_fullpaths(self,fn):
		return map( lambda (rp): os.path.join(self.files_path,rp),
					self.generate_relpaths(fn) )

	def process_incoming(self,op='ln'):
		in_rp = os.path.join(self.files_path, self.in_dir)
		for bn in os.listdir(in_rp):
			src = os.path.join(in_rp,bn)
			self.logger.debug('processing '+src)
			try:
				self.refile(src,op=op)
				# TODO: Caller should remove.  Possible implementation:
				# loop here, but create a new process1 method that can be
				# overridden by subclass and handle success/failure with
				# FilerDone/FilerError
				os.remove(src)
			except Exception as e:
				# instead of logging errors, make them abort
				# (else we won't really pay attention)
				raise
				#self.logger.error(e)
				#self.refile_error(src)

	def refile(self,src,dsts=None,op='ln'):
		if dsts is None:
			# FIXME: This function takes dsts solely for the benefit of
			# refile_errors, which is a thinko.  Do this: move error
			# handling out of this class (incl. refile_error), have dsts
			# determined exlusively within this function, and don't take
			# it as an argument.
			dsts = self.generate_fullpaths(src)
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
		# TODO: errors should be a Filer
		# and moved elsewhere. Perhaps FilerMaster should
		# override refile_error and use FilerError to refile
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
