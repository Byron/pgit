"""Implements the submodule pgit command"""
from base import CmdBase

__all__ = ['SubmoduleCmd']

class SubmoduleCmd(CmdBase):
	"""Provides a CLI for the git-python submodule implementation"""
	#{ Configuration 
	k_class_path = "pgit.cmd.submodule.SubmoduleCmd"
	k_log_application_id = None	# no own logging supported
	
	k_program_name = 'pgit-submodule'
	k_version = "1.0"
	k_usage = '%prog '
	k_description = """Edit or query a git-repository's submodules"""
	#} END configuration
	
	#{Constants
	k_query = 'query'
	k_add = 'add'
	k_remove = 'remove'
	k_move = 'move'
	k_update = 'update'
	#}END constants
	
	def option_parser(self):
		parser = super(SubmoduleCmd, self).option_parser()
		
		return parser
	
	def execute(self, options, args):
		"""Perform the requested operation"""
		cmd = 'query'
		if args:
			cmd = args[0]
		# END handle command parsing
		
		if cmd == self.k_query:
			pass
		elif cmd == self.k_add:
			pass
		elif cmd == self.k_remove:
			pass
		elif cmd == self.k_move:
			pass
		elif cmd == self.k_update:
			pass
		else:
			raise self.parser.error("Invalid operation: %r" % cmd)
		#END handle operation
		
		
