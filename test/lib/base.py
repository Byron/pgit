"""Provide base classes for the test system"""
from test.testlib import TestBase
import git.cmd

import os
import sys
import cStringIO

__all__ = ['TestCmdBase']


class TestCmdBase(TestBase):
	"""Foundation class from which all command test should derive to obtain
	command-specific testing utilities.
	
	These include methods to obtain a configured SpawnedCommand instance which 
	can be called with arguments as if they would be passed from the commanline.
	This has the advantage of executing the command more quickly, but comes at the 
	danger of having it alter the environment of the current interpreter"""
	
	#{ Configuration
	# Type of the command to test. It must be a subclass of BaseCmd
	t_cmd = None
	
	# default arguments to add to the call prior to all passed in arguments
	# Must be a tuple
	k_add_args = tuple()
	#} END configuration
	
	def cmd(self, *args, **kwargs):
		""":return: Instance of your spawned command t_cmd which was provided with
		the given arguments and executed.
		:param kwargs:
			* cwd: Current working dir to set for the duration of the command
			* return_stderr: if True, default False, stderr will be returned additionally
			* fail_on_stderr: if True, default True, we will fail with an 
			  assertion error if the command outputs anything to stderr
		:return: list(linestdout,...) tuple(list(linestdout,...), list(linestderr,...))"""
		assert self.t_cmd is not None, "t_cmd is not set"
		
		cur_dir = os.getcwd()
		os.chdir(kwargs.get('cwd', cur_dir))
		
		sys.stdout = cStringIO.StringIO()
		sys.stderr = cStringIO.StringIO()
		prev_trace = git.cmd.GIT_PYTHON_TRACE
		git.cmd.GIT_PYTHON_TRACE = False
		return_stderr = kwargs.get('return_stderr', False)
		fail_on_stderr = kwargs.get('fail_on_stderr', True)
		
		try:
			self.t_cmd()._execute(*(str(a) for a in self.k_add_args+args))
			err = sys.stderr.getvalue()
			if err and fail_on_stderr:
				raise AssertionError("Command Failed: %s" % err)

			out = sys.stdout.getvalue().splitlines()
			if return_stderr:
				return out, err
			else:
				return out
			# END handle
		finally:
			sys.stdout = sys.__stdout__
			sys.stderr = sys.__stderr__
			git.cmd.GIT_PYTHON_TRACE=prev_trace
			os.chdir(cur_dir)
		# END handle default channels
		
		return self.t_cmd()._execute(*args)
		
	def scmd(self, *args, **kwargs):
		"""Spawn our command with the given *args. **kwargs can be used to configure
		Subprocess.Popen. The output channels will be redirected into pipes which 
		can be read accordingly.
		:return: Started process instance
		:param kwargs:
			cwd: Current working directory"""
		_kwargs = { 'stdout' : subprocess.PIPE, 'stderr' : subprocess.PIPE}
		_kwargs.update(kwargs)
		args = self.k_add_args + args
		return self.t_cmd.spawn(*args, **_kwargs)
			
