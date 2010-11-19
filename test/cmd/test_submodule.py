from pgit.test.lib import *

from pgit.cmd.submodule import *

class TestSubmoduleCmd(TestCmdBase):
	t_cmd = SubmoduleCmd
	
	@with_rw_repo_cmd('HEAD', bare=False)
	def test_base(self, rwrepo, psm):
		# invalid command raises
		self.failUnlessRaises(Exception, psm, 'somecommand')
		
		# no args prints a one-line-per-submodule summary
		out = psm()
		assert len(out) == 1
