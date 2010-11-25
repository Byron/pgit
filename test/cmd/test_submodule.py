from pgit.test.lib import *

from pgit.cmd.submodule import *
from optparse import OptParseError

class TestSubmoduleCmd(TestCmdBase):
	t_cmd = SubmoduleCmd
	
	@with_rw_repo_cmd('HEAD', bare=False)
	def test_base(self, rwrepo, psm):
		# in this test we are quite trusty and just call all known command args
		# and try to trigger arg-based exceptions. The underlying system
		# was tested in detail, so its really just about running the commands code
		
		# QUERY
		#######
		# invalid command raises
		self.failUnlessRaises(OptParseError, psm, 'somecommand')
		
		# no args prints a one-line-per-submodule summary
		out = psm()
		assert out
		
		# query is default mode
		assert psm() == psm(SubmoduleCmd.k_query)
		
		# UPDATE
		########
		# invalid filter raises early
		self.failUnlessRaises(ValueError, psm, SubmoduleCmd.k_update, "doesntexist")
		
		# dry-run does nothing
		psm(SubmoduleCmd.k_update, '-n')
		
		# updates all without anything else
		psm(SubmoduleCmd.k_update)
		
		# only update one, none-recursively, to the latest revision
		psm(SubmoduleCmd.k_update, '--non-recursive', '-l', 'git')
		
		# ADD
		#####
		# too many or too few args
		self.failUnlessRaises(OptParseError, psm, SubmoduleCmd.k_add, "one")
		self.failUnlessRaises(OptParseError, psm, SubmoduleCmd.k_add, ['arg']*4)
		
		sm = rwrepo.submodules[0]
		nsmn = 'newname'
		nsmp = 'newsubmod'
		psm(SubmoduleCmd.k_add, nsmn, nsmp, sm.url, '--branch', 'master')
		
		# url is optional, in case a repository exists - here it doesn't exist
		oname = 'othername'
		self.failUnlessRaises(ValueError, psm, SubmoduleCmd.k_add, oname, 'doesnt_exist')
		
		# it will just return successfully as a submodule with that name
		# already exists
		psm(SubmoduleCmd.k_add, nsmn, nsmp, sm.url)
		
		
		# MOVE
		######
		# not enough args
		self.failUnlessRaises(OptParseError, psm, SubmoduleCmd.k_move, "name")
		
		# move previously created module 
		nsm = rwrepo.submodule(nsmn)
		assert nsm.module_exists()
		assert nsm.path == nsmp
		nsmp += "_moved"
		psm(SubmoduleCmd.k_move, nsm.name, nsmp)
		assert not nsm.module_exists()			# it was moved, our instance is not uptodate
		
		
		# REMOVE
		########
		# need at least one name
		self.failUnlessRaises(OptParseError, psm, SubmoduleCmd.k_remove)
		
		# remove both now submodules - same item multiple time will be fine
		assert nsm.exists()
		
		# dry-run doesn't do anything
		psm(SubmoduleCmd.k_remove, nsm.name, nsm.name, '--force', '--dry-run')
		assert nsm.exists()
		
		psm(SubmoduleCmd.k_remove, nsm.name, nsm.name, '--force')
		assert not nsm.exists()
		
		
		
		
