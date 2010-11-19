"""A diversity of utility functions"""

from test.testlib import (
							with_rw_repo,
							with_rw_and_rw_remote_repo
						)

import os

__all__ = ['with_rw_repo', 'with_rw_and_rw_remote_repo', 'with_rw_repo_cmd']

#{ Decorators

def with_rw_repo_cmd(rev='HEAD', bare=False):
	"""Special decorator compatible with the TestCmdBase. It will alter the decorated
	method so that the first argument is the Repo instance with write access, and 
	the second argument a method which executes the command in-process. The command
	is altered so that the current working directory is set to the passed in repository, 
	unless you override it explicitly. All other args and kwargs passed to it correspond
	to the TestCmdBase.cmd() method"""
	def func_wrapper(func):
		def wrapper(self, rwrepo, *args, **kwargs):
			def cmd_call(*args, **kwargs):
				if 'cwd' not in kwargs:
					kwargs['cwd'] = rwrepo.working_dir
				#END adjust cwd
				return self.cmd(*args, **kwargs)
				# END handle cwd 
			#END cmdcall handler
			return func(self, rwrepo, cmd_call, *args, **kwargs)
		#END wrapper
		wrapped_func = with_rw_repo(rev, bare)(wrapper)
		wrapped_func.__name__ = func.__name__
		return wrapped_func
	#END function wrapper
	return func_wrapper
	
	

#} END decorators

