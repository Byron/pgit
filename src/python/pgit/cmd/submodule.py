"""Implements the submodule pgit command"""
from base import CmdBase

from git import (
					Submodule,
					RootModule,
					RootUpdateProgress,
					InvalidGitRepositoryError
				)

from optparse import OptionGroup

__all__ = ['SubmoduleCmd']

class UpdateProgress(RootUpdateProgress):
	"""Prints all messages to stdout"""
	def update(self, op, index, max_index, message):
		print message
	

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
		
		# UPDATE
		########
		group = OptionGroup(parser, "Update Options")
		
		hlp = """If set, updates will not be handled recursively, but instead only
affect the direct submodules of the curent repository. This usually causes inconsistent
checkouts as children of said submodules might require an update too"""
		group.add_option('--non-recursive' , action='store_true', help=hlp)
		
		hlp = """If set, the sha of the submodule will be ignored. Instead, the
submodule's repository will be updated to the latest available revision"""
		group.add_option('-l', '--to-latest-revision', action='store_true', help=hlp)
		
		hlp = """If set, the given rev-spec defines the commit that should be used 
to be compared against the currently checked-out commit. Otherwise it defaults to HEAD@{1}"""
		group.add_option('--base-commit', default=None, help=hlp)
		parser.add_option_group(group)
		
		
		
		# ADD
		######
		group = OptionGroup(parser, "Add Options")
		hlp = "Specify a tracking branch to use if it is not 'master', which is the default"
		group.add_option('-b', '--branch', help=hlp)
		
		hlp = """If set, the new submodule's repository will be cloned, but not checkedout, i.e.
the working tree is empty"""
		group.add_option('--no-checkout', action='store_true', default=False, help=hlp)
		
		parser.add_option_group(group)
		
		
		# MOVE
		######
		group = OptionGroup(parser, "Move Options", "See Common Options")
		
		parser.add_option_group(group)
		
		
		# REMOVE
		########
		group = OptionGroup(parser, "Remove Options")
		
		hlp = "If set, the submodule's repository will be removed even though it contains modifications"
		group.add_option("--force", action='store_true', default=False, help=hlp)
		
		parser.add_option_group(group)
		
		
		# COMMON
		########
		group = OptionGroup(parser, "Common Options")
		
		hlp  = "If set in remove mode, the submodule's configuration will not be removed, but only its repository\n"
		hlp += "If set in move mode, only the submodule's repository will be moved to the destination.\n"
		hlp += "The configuration will remain unaltered, and is expected to point to the destination path already"""
		group.add_option("--skip-configuration", action='store_true', default=False, help=hlp)
		
		hlp  = "If set in remove mode, the submodule's repository will not be removed and remain on disk\n"
		hlp += "If set in move mode, the submodule's repository will not be moved, only the submodule's configuration will be altered."
		group.add_option('--skip-module', action='store_true', default=False, help=hlp)
		
		hlp = "If set, the operation will be simulated, but not actually performed, i.e. everything remains unchanged.\n"
		hlp += "Only meaningful for update and remove operations."
		group.add_option("-n", "--dry-run", action='store_true', default=False, help=hlp)
		
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
			print "\tbranch: %s" % sm.branch_name
			try:
				mhead = sm.module().head
				fmt = "\thead  : %s"
				if mhead.is_detached:
					msg = (fmt % mhead.commit) + " (detached)"
				else:
					msg = (fmt % mhead.ref) + ((mhead.ref.tracking_branch() is not None and " (tracking %s)" % mhead.ref.tracking_branch().name) or '')
				print msg
			except InvalidGitRepositoryError:
				print "\t(Repository not checked out)"
			#END ignore missing repos
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
		progress = UpdateProgress()
		
		kwargs = dict(
						previous_commit = options.base_commit,
						recursive=not options.non_recursive,
						to_latest_revision=options.to_latest_revision,
						dry_run=options.dry_run,
						progress=progress
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
		if len(args) != 2:
			raise self.parser.error("arguments must be: name destination_path")
			
		name, destpath = args
		sm = self.repo.submodule(name)
		sm.move(destpath, configuration=not options.skip_configuration, module=not options.skip_module)
		print "Successfully moved the repository of submodule %r to %s" % (sm.name, sm.path)
		
	def _exec_remove(self, options, args):
		if len(args) < 1:
			raise self.parser.error("Need a at least one submodule's name to remove")
		#END handle args
		
		for sm in self.repo.submodules:
			if sm.name not in args:
				continue
			#END filter by name
			
			sm.remove(	module=not options.skip_module, 
						configuration=not options.skip_configuration,
						dry_run=options.dry_run,
						force=options.force
					)
		#END for each submodule
	
	#} END handlers
