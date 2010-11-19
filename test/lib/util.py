"""A diversity of utility functions"""

from test.testlib import (
							with_rw_repo,
							with_rw_and_rw_remote_repo
						)

import test.testlib.helper
# apply monkeypatch so that it operates based on this file
test.testlib.helper

import os
from git import Repo
from git.util import join_path

__all__ = ['with_rw_repo', 'with_rw_and_rw_remote_repo', 'with_rw_repo_cmd']

#{ Utilities

def localize_submodules(submodules, source_repo, recursive=True):
	"""Localize the given submodules to use urls as derived from the given source_repo,
	which is assumed to contain a full checkout of all the modules and submodules.
	:param recursive: If True, submodules will be handled recursively. Modules
		will be checked-out as required to get access to the child modules"""
	assert not source_repo.bare, "Source-Repository must not be bare"
	for sm in submodules:
		# need an update, as we commit after each iteration
		sm.set_parent_commit(sm.repo.head.commit)
		smp = join_path(source_repo.working_tree_dir, sm.path)
		sm.config_writer().set_value('url', smp)
		
		if recursive:
			if not sm.module_exists():
				sm.update(recursive=False)
			#END get submodule
			
			localize_submodules(sm.children(), Repo(smp), recursive=True)
		#END handle recursion
		
		# commit after each sm - performance will be fine
		sm.repo.index.commit("Localized submodule paths")
	# END for each submodule
	
	
	

#} END utilities

#{ Decorators

def with_rw_repo_cmd(rev='HEAD', bare=False):
	"""Special decorator compatible with the TestCmdBase. It will alter the decorated
	method so that the first argument is the Repo instance with write access, and 
	the second argument a method which executes the command in-process. 
	The command is altered so that the current working directory is set to the passed in repository, 
	unless you override it explicitly. All other args and kwargs passed to it correspond
	to the TestCmdBase.cmd() method.
	Additionally the submodules contained in the repository are adjusted to pull
	from the local drive, instead of from the remote"""
	def func_wrapper(func):
		def wrapper(self, rwrepo, *args, **kwargs):
			# adjust submodules to point to local destinations on the first level
			localize_submodules(rwrepo.submodules, Repo(os.path.dirname(__file__))) 
			
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

