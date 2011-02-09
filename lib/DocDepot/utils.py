import re, os

def fn_frag(fn,frag_size=2,max_frags=3):
	frags = min( len(fn)/frag_size, max_frags )
	x = map( lambda (i): fn[i*frag_size:(i+1)*frag_size], range(frags) )
	return os.path.join(*x)

def guess_pmid(fn):
	m = re.match( '(?:^|.*/)(\d+)[_\.]', fn )
	if m:
		return m.group(1)
	return None
