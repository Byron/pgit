from pgit.test.lib import *

from pgit.cmd.submodule import *

class TestSubmoduleCmd(TestCmdBase):
	t_cmd = SubmoduleCmd
	
	@with_rw_repo_cmd('HEAD', bare=False)
	def test_base(self, rwrepo, psm):
		# QUERY
		#######
		# invalid command raises
		self.failUnlessRaises(Exception, psm, 'somecommand')
		
		# no args prints a one-line-per-submodule summary
		out = psm()
		assert out
		
		# query is default mode
		assert psm() == psm(SubmoduleCmd.k_query)
		
		# UPDATE
		########
		# invalid filter raises early
		self.failUnlessRaises(ValueError, psm, SubmoduleCmd.k_update, "doesntexist")
		
		# updates all without anything else
		psm(SubmoduleCmd.k_update)
		
		# only update one, none-recursively, to the latest revision
		psm(SubmoduleCmd.k_update, '--non-recursive', '-l', 'git')
		
		# ADD
		#####
		
		
		# MOVE
		######
		
		
		
		# REMOVE
		########
