"""Intialize the pgit package"""
import os
import sys

def init_externals():
	"""Adjust system path to allow access to our externals"""
	ext_path = os.path.join(os.path.dirname(__file__), 'ext')
	
	try:
		import mrv
	except ImportError:
		sys.path.append(ext_path)
		try:
			import mrv
		except ImportError:
			raise EnvironmentError("Failed to setup path to allow mrv to be imported")
		# END handle second import failure
	#END check mrv
	
	def import_git():
		try:
			import git
		except ImportError:
			return False
		#END handle exception
		
		if not hasattr(git, 'RootModule'):
			return False
		# END verify we have full submodule functionality
		return True
	# END utility
	
	# handle git-python
	git_path = os.path.join(ext_path, 'git', 'lib')
	if not import_git():
		sys.path.append(git_path)
		if not import_git():
			raise EnvironmentError("Could not import git, or it was not providing the RootModule type")
		# END handle second attempt
	#END handle git import
	

init_externals()
