#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Forward the call to mrv's setup routine"""
import os

ospd = os.path.dirname
__docformat__ = "restructuredtext"


#{ Initialization

def include_setup_py():
	"""#import mrvs setup.py"""
	# project/setup.py -> project/ext/mrv/setup.py
	setuppath = os.path.join(ospd(os.path.abspath(__file__)) , 'pgit', 'ext', 'mrv', 'setup.py')
	# prevent execution
	
	try:
		execfile(setuppath, globals())
	except Exception, e:
		# lets show the original error
		print "Could not execute setup.py at %r" % setuppath
		raise
	# END exception handling

# main will be executed automatically
include_setup_py()
