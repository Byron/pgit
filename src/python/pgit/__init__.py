"""Intialize the pgit package"""
import os
import sys

def init_externals():
	"""Adjust system path to allow access to our externals"""
	ext_path = os.path.join(os.path.dirname(__file__), 'ext')
	sys.path.insert(0, os.path.join(ext_path, 'mrv'))
	sys.path.insert(0, os.path.join(ext_path, 'gitpython'))
	
	try:
		import mrv
	except ImportError:
		raise EnvironmentError("Failed to setup path to allow mrv to be imported")
	#END check mrv
	
	# verify git version
	try:
		import git
		if not hasattr(git, 'RootModule'):
			raise ImportError("Git's version didn't provide the RootModule")
	except ImportError, e:
		raise EnvironmentError("Could not import git: %s" % str(e))
	#END handle exception
		

init_externals()
