#-*-coding:utf-8-*-
"""
@package pgit.tests.cmd.test_submodule
@brief tests for pgit.cmd.submodule

@author Sebastian Thiel
@copyright [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl.html)
"""
__all__ = []

from bcmd import InputError

from ..lib import with_application
from pgit.tests.lib import *
from pgit.cmd.submodule import *

class TestSubmoduleCommand(TestCmdBase):

    subcommand_name = 'submodule'
    
    @with_application
    def test_base(self):
        # in this test we are quite trusty and just call all known command args
        # and try to trigger arg-based exceptions. The underlying system
        # was tested in detail, so its really just about running the commands code
        
        # QUERY
        #######
        # invalid command raises
        # self.failUnlessRaises(str, psm, ['somecommand'])
        psm = self.cmd

        # simple query - we have no submodules
        out = psm('query')
        # assert not out

        # UPDATE
        ########
        # invalid filter raises early
        assert psm(SubmoduleCommand.OP_UPDATE, "doesntexist")[0] == SubmoduleCommand.ARGUMENT_ERROR
        
        # dry-run does nothing
        psm(SubmoduleCommand.OP_UPDATE, '-n')
        
        # updates all without anything else
        psm(SubmoduleCommand.OP_UPDATE)
        
        # only update one, none-recursively, to the latest revision
        psm(SubmoduleCommand.OP_UPDATE, '--non-recursive', '-l', 'gitpython')
        
        # ADD
        #####
        # too many or too few args
        assert psm(SubmoduleCommand.OP_ADD, "one")[0] == SubmoduleCommand.ARGUMENT_ERROR
        assert psm(SubmoduleCommand.OP_ADD, ['arg']*4)[0] == SubmoduleCommand.ARGUMENT_ERROR
        
        # all the write-tests don't actually work as this repository has no submodules anymore
        # Also it doesn't make much sense to test the argparser, as it is working just fine.

