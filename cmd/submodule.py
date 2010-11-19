"""Implements the submodule pgit command"""
from base import CmdBase

from git import (
					Submodule,
					RootModule
				)

from optparse import OptionGroup

__all__ = ['SubmoduleCmd']

class SubmoduleCmd(CmdBase):
	"""Provides a CLI for the git-python submodule implementation"""
	#{ Configuration 
	k_class_path = "pgit.cmd.submodule.SubmoduleCmd"
	k_log_application_id = None	# no own logging supported
	
	k_program_name = 'pgit-submodule'
	k_version = "1.0"
	k_usage = '%prog operation [flags]'
	k_description = """Edit or query a git-repository's submodules"""
	#} END configuration
	
	#{Constants
	k_query = 'query'
	k_add = 'add'
	k_remove = 'remove'
	k_move = 'move'
	k_update = 'update'
	#}END constants
	
	#{ Base Implementation
	
	def option_parser(self):
		parser = super(SubmoduleCmd, self).option_parser()
		
		group = OptionGroup(parser, "Update Options")
		
		hlp = """If set, updates will not be handled recursively, but instead only
affect the direct submodules of the curent repository. This usually causes inconsistent
checkouts as children of said submodules might require an update too"""
		group.add_option('--non-recursive' , action='store_true', help=hlp)
		
		hlp = """If set, the sha of the submodule will be ignored. Instead, the
submodule's repository will be updated to the latest available revision"""
		group.add_option('-l', '--to-latest-revision', action='store_true', help=hlp)
		parser.add_option_group(group)
		
		
		group = OptionGroup(parser, "Add Options")
		hlp = "Specify a tracking branch to use if it is not 'master', which is the default"
		group.add_option('-b', '--branch', help=hlp)
		
		hlp = """If set, the new submodule's repository will be cloned, but not checkedout, i.e.
the working tree is empty"""
		group.add_option('--no-checkout', action='store_true', default=False, help=hlp)
		
		parser.add_option_group(group)
		
		
		return parser
	
	def execute(self, options, args):
		"""Perform the requested operation"""
		cmd = 'query'
		if args:
			cmd = args[0]
			args = args[1:]
		# END handle command parsing
		
		if cmd == self.k_query:
			self._exec_query(options, args)
		elif cmd == self.k_add:
			self._exec_add(options, args)
		elif cmd == self.k_remove:
			self._exec_remove(options, args)
		elif cmd == self.k_move:
			self._exec_move(options, args)
		elif cmd == self.k_update:
			self._exec_update(options, args)
		else:
			raise self.parser.error("Invalid operation: %r" % cmd)
		#END handle operation
		
	#} END base implementation
	
	
	#{ Handlers
	def _exec_query(self, options, args):
		"""Provide git-submodule like information, but include more information 
		about whether we are tracking anything or not"""
		# 7dd618655c96ff32b5c30e41a5406c512bcbb65f ext/git (0.1.4-586-g7dd6186)
		for sm in self.repo.submodules:
			title = "Submodule: %s" % sm.name 
			print title
			print '-' * len(title)
			print "\tpath  : %s" % sm.path
			print "\turl   : %s" % sm.url
			print "\tbranch: %s" % sm.branch.name
			if sm.module_exists():
				mhead = sm.module().head
				fmt = "\thead  :%s"
				if mhead.is_detached:
					msg = (fmt % mhead.commit) + " (detached)"
				else:
					msg = (fmt % mhead.ref) + (mhead.ref.tracking_branch() is not None and " (tracking)") or '' 
			#END handle module
		#END output each submodule
	
	def _exec_update(self, options, args):
		"""Update the submodules, we allow names of specific ones to be specified as additional args"""
		args = set(args)
		sms = self.repo.submodules
		if args:
			ssms = set(sm.name for sm in sms)
			if len(ssms & args) != len(args):
				raise ValueError("Couldn't find the following submodule's for update: %s" % ", ".join(args - ssms))
			#END issue error
		# END pre-check existance of submodules
		
		kwargs = dict(
						recursive=not options.non_recursive,
						to_latest_revision=options.to_latest_revision
					)
		if not args:
			RootModule(self.repo).update(**kwargs)
		else:
			# only updated specific modules .. smartly,but not based on our root
			for sm in sms:
				if sm.name in args and sm.module_exists():
					RootModule(sm.module()).update(**kwargs)
				# END if name matches filter
			# END for each submodule
		# END handle filter
	
	def _exec_add(self, options, args):
		"""Add a new submodule. The last arg may be the url, which is optional"""
		if len(args) < 2 or len(args) > 3:
			raise self.parser.error("arguments may be: name path [url]")
		# END handle arg count
		
		sm = Submodule.add(self.repo, *args, branch=options.branch, no_checkout=options.no_checkout)
		print "Created submodule %r at path %s" % (sm.name, sm.path)
		
	def _exec_move(self, options, args):
		raise NotImplementedError("todo")
		
	def _exec_remove(self, options, args):
		raise NotImplementedError("todo")
	
	#} END handlers
