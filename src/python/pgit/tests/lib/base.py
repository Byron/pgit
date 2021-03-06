"""Provide base classes for the test system"""
import bapp

from butility.tests import TestCase
from bapp.tests import with_application
import git.cmd
from git import Repo

from pgit import PGitCommand

import os
import sys
import cStringIO

__all__ = ['TestCmdBase', 'with_application']


class TestCmdBase(TestCase):
    """Foundation class from which all command test should derive to obtain
    command-specific testing utilities.
    
    These include methods to obtain a configured SpawnedCommand instance which 
    can be called with arguments as if they would be passed from the commanline.
    This has the advantage of executing the command more quickly, but comes at the 
    danger of having it alter the environment of the current interpreter"""
    
    #{ Configuration

    # The name of the sub-command to use
    subcommand_name = None

    #} END configuration
    
    #{ Overrides
    @classmethod
    def setUpClass(cls):
        """Fix the read-only repo to use ours instead"""
        cls.rorepo = Repo(os.path.dirname(__file__))
        
    #END overrides
    
    #{ Interface
    
    def cmd(self, *args, **kwargs):
        """:return: Instance of your spawned command cmd which was provided with
        the given arguments and executed.
        If you are using this function, you must be sure to use the with_application decorator
        :param kwargs:
            * cwd: Current working dir to set for the duration of the command
            * return_stderr: if True, default False, stderr will be returned additionally
            * fail_on_stderr: if True, default True, we will fail with an 
              assertion error if the command outputs anything to stderr
        :return: list(linestdout,...) tuple(list(linestdout,...), list(linestderr,...))"""
        
        cur_dir = os.getcwd()
        os.chdir(kwargs.get('cwd', cur_dir))
        
        sys.stdout = cStringIO.StringIO()
        sys.stderr = cStringIO.StringIO()
        prev_trace = git.cmd.Git.GIT_PYTHON_TRACE
        git.cmd.Git.GIT_PYTHON_TRACE = False
        return_stderr = kwargs.get('return_stderr', False)
        fail_on_stderr = kwargs.get('fail_on_stderr', False)
        
        cmd = PGitCommand(application=bapp.main())
        
        try:
            returncode = cmd.parse_and_execute(list(str(a) for a in (self.subcommand_name,) + args))
            err = sys.stderr.getvalue()
            if err and fail_on_stderr:
                raise AssertionError("Command Failed: %s" % err)
            # end handle errors right away, if requested

            out = sys.stdout.getvalue().splitlines()
            if return_stderr:
                return returncode, out, err
            else:
                return returncode, out
            # END handle
        finally:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            git.cmd.Git.GIT_PYTHON_TRACE=prev_trace
            os.chdir(cur_dir)
        # END handle default channels
        
        return cmd.parse_and_execute(args)
        
    #} END interface
