import os, random, re, string

#TODO: add collision versioning, add #2, #3, ...

def fn_frag(fn,frag_size=2,max_frags=3):
	frags = min( len(fn)/frag_size, max_frags )
	x = map( lambda (i): fn[i*frag_size:(i+1)*frag_size], range(frags) )
	return os.path.join(*x)

def guess_pmid(fn):
	m = re.match( '(?:^|.*/)(\d+)[_\.]', fn )
	if m:
		return m.group(1)
	return None

def unique_name(fn):
	def _random_string(N=6):
		return ''.join(random.choice(
			string.ascii_lowercase + string.digits) for x in range(N))
	root,ext = os.path.splitext(fn)
	return os.path.join( os.path.basename(root)+'#'+_random_string()+ext )

def next_version(path):
	"""return path if not exists, or next path#i if it does"""
	root,ext = os.path.splitext(path)
	i = 1
	while os.path.exists(path):
		path = root + '#' + str(i) + ext
		i += 1
	return path



if __name__ == '__main__':
	p = '/tmp/next_version.txt'
	print unique_name(p)
