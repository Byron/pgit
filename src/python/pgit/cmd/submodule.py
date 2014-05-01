#-*-coding:utf-8-*-
"""
@package pgit.cmd.submodule
@brief Implements the submodule pgit command

@author Sebastian Thiel
@copyright [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl.html)
"""
__all__ = ['UpdateProgress', 'SubmoduleCommand']

import bapp
from butility import Version
from bcmd import InputError

from .base import PGitSubCommand

from git import ( Submodule,
                  RootModule,
                  RootUpdateProgress,
                  InvalidGitRepositoryError )

__all__ = ['SubmoduleCommand']


class UpdateProgress(RootUpdateProgress):
    """Prints all messages to stdout."""

    def __init__(self, *args, **kwargs):
        self.log = kwargs.pop('log')
        super(UpdateProgress, self).__init__(*args, **kwargs)

    def update(self, op, index, max_index, message):
        self.log.info(message)
    

class SubmoduleCommand(PGitSubCommand, bapp.plugin_type()):
    """Provides a CLI for the git-python submodule implementation"""
    # -------------------------
    ## @name Configuration
    # @{
    
    name = 'submodule'
    version = Version('1.0')
    description = "Edit or query a git-repository's submodules"

    ## -- End Configuration -- @}

    # -------------------------
    ## @name Constants
    # @{

    OPERATION = 'operation'
    
    OP_QUERY = 'query'
    OP_ADD = 'add'
    OP_REMOVE = 'remove'
    OP_MOVE = 'move'
    OP_UPDATE = 'update'

    ## -- End Constants -- @}


    # -------------------------
    ## @name Base Implementation
    # @{

    def setup_argparser(self, parser):
        """Default implementation adds nothing. This is common if you use subcommands primarily"""
        super(SubmoduleCommand, self).setup_argparser(parser)

        help = """The submodule command allows you to interact with git-submodules, that is you may query data about
them, as well as change them in a variety of ways.

The main benefit of this implementation is its ability to update submodules keeping the actual change in mind, 
which allows you to synchronize your submodules the same way as git synchronizes the rest of your working tree.

Have a look at https://github.com/Byron/pgit/blob/master/src/md/submodule.md for more details"""
        subparsers = parser.add_subparsers(title='Operation',
                                           dest=self.OPERATION,
                                           description=help)
        
        # QUERY
        ########
        # This should be default, but we can't specify it. Fair enough
        help = "List all submodule information"
        sp = subparsers.add_parser(self.OP_QUERY, description=help, help=help)


        # UPDATE
        ########
        help = "Update re-synchronizes all submodules recursively, assuring that your working- tree including all \
submodules corresponds to the state stored in the repository. This will properly deal with removed, added and \
changed submodules as well."
        sp = subparsers.add_parser(self.OP_UPDATE, description=help, help=help)


        help = "If set, updates will not be handled recursively, but instead only \
affect the direct submodules of the curent repository. This usually causes inconsistent \
checkouts as children of said submodules might require an update too"
        sp.add_argument('--non-recursive', action='store_true', default=False, help=help)
        
        help = "Instead of using the submodule's sha as hint to which revision to update the submodule's repository,\
update it the latest available revision in the remote repository."
        sp.add_argument('-l', '--to-latest-revision', action='store_true', help=help)
        
        help = "Specifies the commit rev-spec to use (e.g. HEAD~1, ORIG_HEAD, HEAD@{1}) as basis for the comparison \
with the currently checked-out commit in the root-repository. From the difference of the commits the command \
determines the changes."
        sp.add_argument('--base-commit', default=None, help=help)

        help  = "If set, the operation will be simulated, but not actually performed, "
        help += "i.e. everything remains unchanged."
        sp.add_argument('-n', '--dry-run', action='store_true', default=False, help=help)

        help  = "Optional submodules which should be updated selectively. If unset, "
        help += "all submodules will be updated unconditionally"
        sp.add_argument('names', nargs='*', metavar='submodule', help=help)

        
        # ADD
        ######
        help = "Add an existing or newly checked-out submodule to the current git repository."
        sp = subparsers.add_parser(self.OP_ADD, description=help, help=help)

        help = "Specify a tracking branch to use, like 'master'. If unset, there will be no tracking branch."
        sp.add_argument('-b', '--branch', default=None, help=help)
        
        help  = "If set, the new submodule's repository will be cloned, but not checkedout,"
        help += "i.e. the working tree is empty"
        sp.add_argument('--no-checkout', action='store_true', default=False, help=help)

        help = "The name of the newly added submodule"
        sp.add_argument('name', help=help)

        help = "Path at which the submodule was checked out, or will be checked out if url is given too."
        sp.add_argument('path', help=help)

        help = "The url from which to clone the submodule, in case it doesn't exist at 'path'"
        sp.add_argument('url', nargs='?', default=None, help=help)


        # MOVE
        ######
        help = "The move operation allows you to move the submodule's repository to a different place in the \
repository. This effectively changes the path at which it resides"
        sp = subparsers.add_parser(self.OP_MOVE, description=help, help=help)

        help  = "Only the submodule's repository will be moved to the destination."
        help += "The configuration will remain unaltered, and is expected to point to the destination path already."
        sp.add_argument('--skip-configuration', action='store_true', default=False, help=help)

        help  = "The submodule's repository will not be moved, "
        help += "only the submodule's configuration will be altered."
        sp.add_argument('--skip-module', action='store_true', default=False, help=help)

        help = "The name of the submodule to move"
        sp.add_argument('name', help=help)

        help = "A path relative to your parent repository root to which to move the submodule"
        sp.add_argument('destination_path', help=help)
        
        # REMOVE
        ########
        help = "The operation removes an existing submodule. It will, by default, not remove the submodule's \
repository if it contains any user modifications"
        sp = subparsers.add_parser(self.OP_REMOVE, description=help, help=help)
        
        help = "If set, the submodule's repository will be removed even though it contains modifications"
        sp.add_argument('--force', action='store_true', default=False, help=help)

        help  = "The submodule's configuration will not be removed, but only its repository."
        help += "The configuration will remain unaltered, and is expected to point to the destination path already."
        sp.add_argument('--skip-configuration', action='store_true', default=False, help=help)

        help  = "The submodule's repository will not be removed and remain on disk."
        help += "only the submodule's configuration will be altered."
        sp.add_argument('--skip-module', action='store_true', default=False, help=help)

        help  = "If set, the operation will be simulated, but not actually performed, "
        help += "i.e. everything remains unchanged."
        sp.add_argument('-n', '--dry-run', action='store_true', default=False, help=help)

        help = "One or more names of submodules to remove"
        sp.add_argument('names', nargs='+', help=help)

        
        return self

    ## -- End Base Implementation -- @}
    
    def execute(self, args, remaining_args):
        """Perform the requested operation"""
        cmd = args.operation
        
        try:
            {self.OP_QUERY : self._exec_query,
             self.OP_ADD   : self._exec_add,
             self.OP_REMOVE: self._exec_remove,
             self.OP_MOVE  : self._exec_move,
             self.OP_UPDATE: self._exec_update}[cmd](args)
        except KeyError:
            raise InputError("Invalid operation: %r" % cmd)
        #END handle operation
        
    #{ Handlers
    def _exec_query(self, args):
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
    
    def _exec_update(self, args):
        """Update the submodules, we allow names of specific ones to be specified as additional args"""
        names = set(args.names)
        sms = self.repo.submodules
        if names:
            ssms = set(sm.name for sm in sms)
            if len(ssms & names) != len(names):
                raise InputError("Couldn't find the following submodule's for update: %s" % ", ".join(names - ssms))
            #END issue error
        # END pre-check existance of submodules
        progress = UpdateProgress(log=self.log())
        
        kwargs = dict( previous_commit = args.base_commit,
                       recursive=not args.non_recursive,
                       to_latest_revision=args.to_latest_revision,
                       dry_run=args.dry_run,
                       progress=progress )
        
        if not names:
            RootModule(self.repo).update(**kwargs)
        else:
            # only updated specific modules .. smartly,but not based on our root
            for sm in sms:
                if sm.name in names and sm.module_exists():
                    # As RootModule will ignore the parent module :(, we have to try to 
                    # get a pull done. Will just use git for that
                    smm = sm.module()
                    if not smm.head.ref.tracking_branch():
                        self.log().info("Can't update submodule '%s' as there is no tracking branch", sm.name)
                    else:
                        # end handle missing tracking setup
                        try:
                            if args.dry_run:
                                self.log().info("WOULD pull '%s' submodule", sm.name)
                            else:
                                self.log().info("Pulling submodule '%s'", sm.name)
                                smm.git.pull()
                            # end handle dryrun
                        except GitCommandError, err:
                            self.log().debug("Failed to pull submodule '%s' with error: %s", sm.name, str(err))
                        # end ignore exceptions
                    # end handle has tracking branch setup
                    RootModule(smm).update(**kwargs)
                # END if name matches filter
            # END for each submodule
        # END handle filter
    
    def _exec_add(self, args):
        """Add a new submodule. The last arg may be the url, which is optional"""
        sm = Submodule.add(self.repo, args.name, args.path, args.url, branch=args.branch, no_checkout=args.no_checkout)
        self.log().info("Created submodule %r at path %s", sm.name, sm.path)
        
    def _exec_move(self, args):
        sm = self.repo.submodule(args.name)
        sm.move(args.destination_path, configuration=not args.skip_configuration, module=not args.skip_module)
        self.log().info("Successfully moved the repository of submodule %r to %s", sm.name, sm.path)
        
    def _exec_remove(self, args):
        for sm in self.repo.submodules:
            if sm.name not in args.names:
                continue
            #END filter by name
            
            sm.remove(  module=not args.skip_module, 
                        configuration=not args.skip_configuration,
                        dry_run=args.dry_run,
                        force=args.force
                    )
        #END for each submodule
    
    #} END handlers

# end class SubmoduleCommand
