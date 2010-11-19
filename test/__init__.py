
import git

import os
import sys

def init_git():
	"""Assure that the git-python test-system is available to us"""
	# use our external module by default
	ospd = os.path.dirname
	test_path = os.path.join(ospd(ospd(__file__)), 'ext', 'git')
	
	sys.path.insert(0, test_path)
	try:
		import test.testlib
	except ImportError:
		raise EnvironmentError("Couldn't import git-python test library")
	#END handle testlibrary import
	

init_git()