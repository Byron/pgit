#-*-coding:utf-8-*-
"""
@package pgit.cmd.base
@brief Provides base types that should be used by all pgit commands

@author Sebastian Thiel
@copyright [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl.html)
"""
__all__ = ['PGitCommand', 'PGitSubCommand']

from bcmd import CommandBase
from butility import Version

from git import Repo
import os

__all__ = ['PGitCommand']

#{Classes

class PGitCommand(CommandBase):
    """Implements functinality common to all pgit commands
    
    We initialize a member called 'repo' which provides a Repo instance based on 
    the current working directory"""

    # -------------------------
    ## @name Configuration
    # @{

    ## Name of our program
    name = 'pgit'
    ## A version string
    version = Version('0.1.0')
    ## command description
    description = "The main pgit command - functionality comes in with subcommands"
    
    ## -- End Configuration -- @}

#}END classes


class PGitSubCommand(PGitCommand):
    """A pgit subcommand should derive from this type, setting its name member accordingly"""

    # -------------------------
    ## @name Configuration
    # @{

    main_command_name = PGitCommand.name
    
    ## -- End Configuration -- @}


    # -------------------------
    ## @name Subclass Overrides
    # @{

    ## To be set by subclass
    name = None
    
    ## -- End Subclass Overrides -- @}
    

    def __init__(self, *args, **kwargs):
        super(PGitSubCommand, self).__init__(*args, **kwargs)
        self.repo = Repo(os.getcwd())

# end class PGitSubCommand
